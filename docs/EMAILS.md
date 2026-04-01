### Email 1: Internal Request & Context for Approval (Forward to Christina)

**To:** [Internal Google Team CC'd on original thread]
**Subject:** Re: Build with AI, Build a 3D Flight Simulator - Request for external sharing approval

Hi team,

Mark Pralat (based in Boston) reached out asking for the recording, slides, and codelab for our recent Infinite Flight Simulator event since he couldn't attend in person.

Could someone please forward this thread to Christina (DevRel Manager) to get her official sign-off for sharing the GitHub repo and codelab externally? I’ve included a quick summary below to make it easy for her to review.

Thanks!
Jorge

---
**[Context for Christina]**

Hi Christina,

We are getting inbound requests from developers outside our region (like Mark below) who want to learn from the "Build with AI: 3D Flight Simulator" workshop. 

To support them and scale our impact, I have polished the project into a self-paced, 6-module Codelab. It serves as a fantastic, hands-on showcase for **Gemini 2.5 Flash, Imagen 3, and Google Earth Engine** within a Service-Oriented Architecture. 

*   **Security:** The repo is completely scrubbed of credentials and enforces Google Cloud Secret Manager for all API keys.
*   **Readiness:** The codebase and Markdown guides are fully tested, modularized, and ready for public consumption.
*   **Impact:** Allows us to expand the "Build with AI" initiative to developers globally who cannot attend in-person events.

Could we get your approval to share the GitHub repository and slides externally? 

Best,
Jorge

---

### Email 2: Reply to Mark (Draft to send *after* Christina's approval)

**To:** Mark Pralat
**Subject:** Re: Build with AI, Build a 3D Flight Simulator

Hi Mark,

Thanks for reaching out! It's awesome to hear you're interested all the way from Boston.

The first event wasn't recorded, unfortunately, but I have some good news: we've put together a self-paced codelab and open-sourced the repository so anyone can build the simulator from scratch.

You can find the resources here:
- **GitHub Repository:** [https://github.com/gdg/infinite-loop-simulator](https://github.com/gdg/infinite-loop-simulator)
- **Codelab Guide:** The `/codelab` directory in the repository contains a step-by-step 6-module curriculum.
- **Slides:** You can find the slide deck in the `/docs` folder.

We recently pushed a "Service-Oriented" refactor which makes the architecture much easier to follow. Since you're interested in how we handle the "Infinite Loop" memory management and the Vertex AI integration, I'd recommend starting with **Module 4 (AI Vision)** and **Module 6 (Agentic Intelligence)**.

Feel free to open an issue on the repo or reply here if you have any questions as you dive in!

Best,
Jorge
GDG Lead / Build with AI Organizer