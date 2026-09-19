const copyLinkButton =
    document.querySelector(".copy-link");

if (copyLinkButton) {

    copyLinkButton.addEventListener("click", async () => {

        const url =
            copyLinkButton.dataset.url;

        try {

            await navigator.clipboard.writeText(url);

            copyLinkButton.textContent =
                "Copied!";

            setTimeout(() => {

                copyLinkButton.textContent =
                    "Copy link";

            }, 2000);

        } catch (error) {

            copyLinkButton.textContent =
                "Unable to copy";

        }

    });

}