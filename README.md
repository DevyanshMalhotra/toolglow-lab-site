# ToolGlow Lab

**Smarter tools. Less busywork.**

A buildless, static website for ToolGlow Lab and its privately operated desktop application, **ToolGlow Lab Automation**. HTML5, CSS3, system fonts, and local artwork; no JavaScript, packages, cookies, analytics, external fonts, or video embeds. GitHub Pages is the intended host; no paid service or custom domain is needed to host the website.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | Brand, content categories, original Shorts, desktop app explanation, contact |
| `privacy.html` | Google/YouTube data use, scopes, local storage, retention, revocation, manual deletion |
| `terms.html` | Terms for the informational site and private project |
| `styles.css` | Responsive layout, keyboard focus, reduced motion, print and forced-color support |
| `404.html` | GitHub Pages error page, including links that work under nested missing paths |
| `assets/favicon.svg` | Local vector brand icon |
| `assets/social.png` | Local 1200 × 630 social-sharing image |
| `sitemap.xml` | Public page URLs |
| `.nojekyll` | Disable Jekyll processing |
| `.gitignore` | Exclude local QA output and common credential/video files |
| `scripts/validate_site.py` | Read-only structure, links, CSS syntax, and secret-pattern checks |

No channel handle is guessed. Add a YouTube channel link only after the owner confirms its canonical channel URL. The homepage artwork is illustrative, not a published video or functioning player.

## Local preview

From this repository, run `python -m http.server 8000 --bind 127.0.0.1` and open `http://127.0.0.1:8000/`. No installation or build is needed. The 404 page deliberately uses the deployment prefix `/toolglow-lab-site/`; preview it under that prefix to test its links.

Optional developer validation uses the already available Python packages Beautiful Soup and tinycss2: `python scripts/validate_site.py`. These are QA tools only and are not website dependencies. Check keyboard navigation, the narrowest mobile width, both legal pages, and reduced-motion behavior in a browser after changes.

## GitHub Pages deployment

Repository: [DevyanshMalhotra/toolglow-lab-site](https://github.com/DevyanshMalhotra/toolglow-lab-site).

Use branch publishing from **`main` → `/ (root)`**. A push to `main` updates the site after the Pages build completes. The expected address is `https://devyanshmalhotra.github.io/toolglow-lab-site/`; an expected address is not proof of deployment. Confirm the Pages build and HTTPS responses before using the URLs in Google Cloud.

If automatic enablement is unavailable:

1. Open [repository Settings → Pages](https://github.com/DevyanshMalhotra/toolglow-lab-site/settings/pages), signed in as a repository administrator.
2. In **Build and deployment → Source**, select **Deploy from a branch**.
3. Select **main**, then **/ (root)**, and click **Save**.
4. Leave **Custom domain** empty. Enable **Enforce HTTPS** when available.
5. Wait for **pages build and deployment** to succeed in the repository’s **Actions** tab.
6. Visit the URL shown by Pages. Confirm the homepage, `privacy.html`, `terms.html`, `styles.css`, and `assets/social.png` load. Check a nonexistent nested path displays the styled 404 page and working home/legal links.

The repository is public. GitHub Pages branch publishing for public repositories is available on GitHub Free; no extra subscription is required. See [GitHub’s publishing-source documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Google OAuth setup and remaining restrictions

Official documentation reviewed on **November 14, 2026**. Publishing this website does **not** complete OAuth branding verification, scope verification, domain ownership verification, or any YouTube API review. No Google Cloud settings or private automation code are changed by this repository.

1. In the correct Google Cloud project, enable **YouTube Data API v3**. Keep testing and production projects separate as required by [Google’s OAuth policies](https://developers.google.com/identity/protocols/oauth2/policies).
2. In **Google Auth Platform → Branding**, use **ToolGlow Lab Automation**, support email `jaiseetaramsabhiko@gmail.com`, and a monitored developer contact address. The homepage visibly connects this application name to ToolGlow Lab. Do not upload a fabricated certification or verification badge.
3. After deployment is confirmed, the intended branding URLs are:
   - Homepage: `https://devyanshmalhotra.github.io/toolglow-lab-site/`
   - Privacy Policy: `https://devyanshmalhotra.github.io/toolglow-lab-site/privacy.html`
   - Terms: `https://devyanshmalhotra.github.io/toolglow-lab-site/terms.html`
4. **Domain ownership is unresolved.** [Google’s brand-verification requirements](https://developers.google.com/identity/protocols/oauth2/production-readiness/brand-verification) require ownership verification of authorized domains, using an appropriate Google Search Console owner associated with the Cloud project. Having a GitHub repository, a `github.io` URL, or a Search Console URL-prefix property does not by itself establish acceptance of that domain for OAuth verification. Do not claim ownership of `github.io`. Check the actual domain Google accepts and the verification result. This task neither buys nor assumes an owned domain. If Google rejects the shared-hosting domain, full brand verification remains blocked until an eligible domain under your control is available or Google confirms another accepted path. Static hosting can remain free on GitHub Pages.
5. In **Audience**, choose the configuration that reflects actual use. A private desktop app using a personal Gmail account is not automatically an **Internal** Google Workspace app. For external testing, add only the intended operator/test accounts. Testing refresh tokens for these YouTube scopes expire after seven days; see [Google’s token-expiration documentation](https://developers.google.com/identity/protocols/oauth2#expiration).
6. In **Data Access**, request only the actual scopes: `https://www.googleapis.com/auth/youtube.upload` and `https://www.googleapis.com/auth/youtube.readonly`. Their permissions are broader than the operations used here. Confirm the Cloud Console’s current classification and requirements; do not add broad scopes to avoid a review. [Google’s scope reference](https://developers.google.com/identity/protocols/oauth2/scopes#youtube) describes the permissions.
7. Review [Google’s personal-use verification exception](https://developers.google.com/identity/protocols/oauth2/production-readiness/sensitive-scope-verification#exceptions_to_verification_requirements). It may apply to an operator-only application. It does not remove platform policies, unverified-app warnings, account caps, or automatically approve branding. Do not expand access based on that exception without reassessing eligibility.
8. Use an OAuth client of type **Desktop app** and the installed-app authorization flow. This static website is not an OAuth callback handler. Never put the client JSON, tokens, account-access files, or authorization codes in this repository. Do not add web origins or redirect URIs merely to make a desktop application look like a web application. See [Google’s native-app OAuth guide](https://developers.google.com/identity/protocols/oauth2/native-app).
9. Before requesting verification or broadening use, verify the **actual desktop implementation** matches the published policy. No private app source was supplied for this website work. Confirm its exact endpoints, fields, local permissions, logs/copies, authorized channel, chosen video visibility, user consent before uploads, and handling of revocation. Review whether `youtube.readonly` remains necessary for the actual calls; change both code and disclosures together if it is not.
10. Carry out the policy’s manual deletion process; the website cannot erase files from the operator’s computer. Apply YouTube’s API-data retention rules, including the applicable 30-day refresh/delete rule and seven-day deletion requirement. Verify local logs and copies as well as token files. Distinguish cached API data from original videos and videos hosted on YouTube. See [YouTube Developer Policies](https://developers.google.com/youtube/terms/developer-policies).
11. Check current [YouTube upload documentation](https://developers.google.com/youtube/data/reference/rest/v3/videos/insert), API project status, quotas, and any applicable compliance review separately. Do not equate an OAuth approval with a YouTube API approval or assume an upload’s visibility from an old restriction. Test uploads only with the operator’s explicit intended content and settings; this website task does not upload videos.

## Public/private boundary

Keep the automation application and all its runtime data outside this repository. `.gitignore` is a precaution, not a security boundary: inspect each staged file before committing. Do not add environment files, client credentials, tokens, private channel/video records, generated media, screenshots containing account data, or private logs.

The privacy text is based on the desktop behavior described by the project owner. It promises no encryption-at-rest system, certification, automatic deletion tool, public onboarding, or verified Google status. The operator must keep the published policy aligned with the real implementation and fulfill its stated procedures.

## Validation performed — November 14, 2026

- W3C Nu HTML Checker: all four HTML documents passed with **zero errors and zero warnings**.
- Read-only local validator: **1,544 checks passed**, including unique IDs, local files and fragments, named links/navigation, landmarks, headings, footer links, CSS parsing, reduced-motion/focus rules, and common credential patterns. Pattern scanning is not an exhaustive secret audit.
- Installed Microsoft Edge in headless mode: homepage, both legal pages, and nested 404 tested at **320, 375, 390, 768, 1024, and 1440 CSS pixels** (24 combinations). No horizontal overflow, external resources, runtime errors, or failed resource requests were observed.
- Browser checks confirmed no scripts, cookies, or local-storage entries; visible keyboard focus on the skip link; working skip and section anchors; and disabled animation/smooth scrolling with reduced motion enabled.
- Desktop (1440px), tablet (768px), mobile (390px), and mobile privacy screenshots were inspected. No physical-device or screen-reader certification is claimed.
- `git diff --check` passed. Only public website source, local artwork, and maintenance documentation/tools are included; no private automation files were inspected or added.

Contact: [jaiseetaramsabhiko@gmail.com](mailto:jaiseetaramsabhiko@gmail.com).
