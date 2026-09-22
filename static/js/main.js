/*
 * Faithbuilders — front-end behaviour
 *
 * Progressive enhancement only: every page works without JavaScript,
 * this file just adds small conveniences on top.
 */

// "Copy link" button on the post detail page.
// Copies the article URL to the clipboard and briefly confirms it.
const copyLinkButton = document.querySelector(".copy-link");

if (copyLinkButton) {
    copyLinkButton.addEventListener("click", async () => {
        const url = copyLinkButton.dataset.url;

        try {
            await navigator.clipboard.writeText(url);

            // Momentary "Copied!" feedback, then restore the label.
            copyLinkButton.textContent = "Copied!";

            setTimeout(() => {
                copyLinkButton.textContent = "Copy link";
            }, 2000);
        } catch (error) {
            // Clipboard access can be blocked (e.g. insecure origin).
            copyLinkButton.textContent = "Unable to copy";
        }
    });
}
