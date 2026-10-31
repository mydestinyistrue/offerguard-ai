import * as pdfjsLib from 'pdfjs-dist';
import pdfjsWorker from 'pdfjs-dist/build/pdf.worker.min.mjs?url';
import Tesseract from 'tesseract.js';

// Configure PDF.js worker
pdfjsLib.GlobalWorkerOptions.workerSrc = pdfjsWorker;

let cachedWorker = null;

/**
 * Get or initialize a reusable Tesseract worker for high performance.
 */
export async function getTesseractWorker(onProgress) {
  if (!cachedWorker) {
    cachedWorker = await Tesseract.createWorker(['eng', 'hin'], undefined, {
      logger: (m) => {
        if (onProgress && m.status === 'recognizing text') {
          onProgress(`OCR progress: ${Math.round((m.progress || 0) * 100)}%`);
        }
      },
    });
  }
  return cachedWorker;
}

/**
 * Terminate the cached worker if needed (e.g. on unmount or clear).
 */
export async function terminateTesseractWorker() {
  if (cachedWorker) {
    try {
      await cachedWorker.terminate();
    } catch {
      // ignore
    }
    cachedWorker = null;
  }
}

/**
 * Extract text from an image file (PNG, JPG, WebP, etc.).
 */
export async function processImageFile(file, onProgress) {
  const worker = await getTesseractWorker(onProgress);
  const ret = await worker.recognize(file);
  return (ret.data?.text || '').trim();
}

/**
 * Extract text from a PDF file.
 * Handles both digital text PDFs and scanned / image-only PDFs using canvas rendering + OCR.
 */
export async function processPdfFile(file, onProgress) {
  const worker = await getTesseractWorker(onProgress);
  const arrayBuffer = await file.arrayBuffer();
  
  const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
  const pdf = await loadingTask.promise;
  const numPages = pdf.numPages;
  const pageTexts = [];

  for (let pageNum = 1; pageNum <= numPages; pageNum++) {
    if (onProgress) {
      onProgress(`Reading PDF page ${pageNum} of ${numPages}...`);
    }

    const page = await pdf.getPage(pageNum);

    // 1. First attempt: extract digital text if present
    let digitalText = '';
    try {
      const textContent = await page.getTextContent();
      digitalText = textContent.items
        .map((item) => ('str' in item ? item.str : ''))
        .filter(Boolean)
        .join(' ')
        .replace(/\s+/g, ' ')
        .trim();
    } catch (err) {
      console.warn(`Could not extract digital text from page ${pageNum}:`, err);
    }

    // If page already has rich digital text (> 50 chars), keep it
    if (digitalText.length > 50) {
      pageTexts.push(digitalText);
      continue;
    }

    // 2. Second attempt: page is scanned or contains embedded images/screenshots!
    // Render the PDF page onto a 2x resolution canvas and run Tesseract OCR
    if (onProgress) {
      onProgress(`Running OCR on scanned/image PDF page ${pageNum} of ${numPages}...`);
    }

    try {
      const viewport = page.getViewport({ scale: 2.0 }); // 2x scale for crisp OCR accuracy
      const canvas = document.createElement('canvas');
      canvas.width = viewport.width;
      canvas.height = viewport.height;
      const ctx = canvas.getContext('2d');

      const renderContext = {
        canvasContext: ctx,
        viewport: viewport,
      };

      await page.render(renderContext).promise;

      // Recognize text from rendered canvas image
      const ocrResult = await worker.recognize(canvas);
      const ocrText = (ocrResult.data?.text || '').trim();

      if (ocrText) {
        pageTexts.push(ocrText);
      } else if (digitalText) {
        pageTexts.push(digitalText);
      }
    } catch (err) {
      console.error(`OCR failed on page ${pageNum}:`, err);
      if (digitalText) {
        pageTexts.push(digitalText);
      }
    }
  }

  return pageTexts.join('\n\n').trim();
}
