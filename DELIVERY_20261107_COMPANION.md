# Recolio support-site companion update — 2026-11-07

Repository: kevincy/Recolio-support, branch main, baseline fe90160. Existing untracked .DS_Store is preserved and excluded. No App code, identifiers, purchases, FSRS, readiness, database or ASC changes.

## Actual update

- Six-language cat-led homepage, real Today hero, Teach walkthrough, saved-explanation story and user-controlled localized video. Existing import, image-text search, named folders and optional Pro iCloud sections remain.
- All 30 old website screenshot files replaced with current companion-launch captures; 18 new Today/Teach/saved derivatives added. Six previously reviewed native App demonstration videos copied unchanged. No fabricated UI, new artwork, analytics or external video host. Videos are silent edits combining actual App footage with UI screenshot holds; not live dictation demonstrations.
- Guide grows from 10 to 14 sections; support FAQ grows from 6 to 9 answers per language. Topics: own-word explanation, compare/add/self-assess, direct dictation into the editor, permissions/fallback, optional reminders, companion/motion controls and local storage limits.
- Privacy section 2 gains companion/dictation/notification details in all six languages, keeping 11 numbered sections. Terms retain 12 sections and commercial terms; shared updated-date labels reflect the refreshed documentation.
- UI language routing/legacy zh compatibility retained. Video uses controls, no autoplay, preload none; language change pauses videos outside the chosen locale.

## Source verification

App sources under ../Remin-NA:
- ReminApp/Views/MainViews.swift: TeachCardSheet and Today companion entries; comparison/self-assessment/save stages.
- ReminApp/Services/TeachSpeechInput.swift: requiresOnDeviceRecognition; direct transcription and discard/manual-edit preservation regressions.
- ReminApp/Services/ReviewReminders.swift: enabled false; first-use 20:00 slot on, 08:00/12:30 off; includesDeckNames false by default; real-count refresh and cancellation owner.
- ReminApp/Services/ImportExport.swift: local Teach records excluded/cleared during library restore; reimport cannot rebind old records.
- docs/RECOLIO_COMPANION_VISUAL_REFRESH.md and docs/appstore/RECOLIO_COMPANION_LAUNCH_REFRESH_20261106.md.
- Screenshot/video source: screenshots/recolio-companion-launch-20261106; hashes and dimensions in assets/screenshots/manifest.json and assets/videos/manifest.json.

Accuracy boundaries: cat does not grade correctness; Teach is separate from FSRS/normal completed-review counts. Explanation drafts/history are local-only and excluded from iCloud/backup; card deletion and library restore can remove them. Dictation requires permissions and on-device language/device support, never promises cloud fallback. Reminders are optional and system delivery is not guaranteed. iCloud is off by default and requires Pro; existing free/import limits are unchanged.

## Executed validation

- python3 scripts/build.py: PASS, five routes and six locales.
- python3 scripts/check_site.py: PASS, 30 localized route variants, 48 image hashes, six video hashes, 14 guide sections/9 FAQ answers, local anchors/gallery/poster/media references and policy section counts.
- tests/language.test.cjs: PASS 122/122, using installed runtime Node.
- tests/browser.cjs: PASS 60 page/locale/viewport combinations (390 and 1280 px), image decode, localized video metadata/duration 15–17 seconds, no autoplay, responsive overflow, tour controls, language persistence and localized links.
- Browser rerun after shorter Chinese hero copy and actual image dimensions: PASS same 60 cases. First shell attempt could not find node; rerun used its installed absolute path. Sandbox initially denied preview-server socket; normal escalated local preview succeeded.
- Browser screenshots under /tmp/recolio-support-review-20261107; en desktop and zh-Hant mobile homepage visually inspected. Additional Teach section captures supplement the homepage checks.
- git diff --check and build freshness checked before commit.

No full App UI, maximum-font, CloudKit, StoreKit, microphone, device-notification tests performed: outside this static-site change. New language copy has editorial/AI review, not human native-speaker sign-off or legal approval. No new product-efficacy claims.

Deployment: main push triggers existing GitHub Pages workflow. Actual push/deployment outcome is reported separately; local checks alone do not prove the public site has updated.
