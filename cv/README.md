# Kajal CV and project technical portfolio (draft)

The deliverable has two sections:

1. Page 1: a concise CV with education, profile and a project index.
2. Pages 2-7: one detailed page per runnable project with the structure, architecture, data flow, implementation, limitations and run instructions.

`Kajal_Kale_CV.pdf` is the printable seven-page A4 document. `Kajal_Kale_CV.html` is the responsive website version with jump links and print styling. The `diagrams/` folder contains twelve reusable SVG images, one architecture image and one data flow image per project. Keep this folder alongside the HTML file so the images load. The PDF contains vector diagrams directly and works on its own.

To update descriptions, change the `PROJECTS` entries in `generate_cv.py` and run `python cv/generate_cv.py` from the repository root. Python needs `reportlab` installed for PDF generation. The generated HTML, PDF and diagrams should be updated together.

Before applying, Kajal must add her own email, city, college, dates, verified skills and personal GitHub profile. The DRAFT notice should remain until verified. These are prepared learning examples, not claims of employment or independent authorship. She should run and modify projects, then describe only the parts she personally contributed and can explain.
