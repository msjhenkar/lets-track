chrome.tabs.query(
    {
        active: true,
        currentWindow: true
    },

    function(tabs) {

        const activeTab = tabs[0];


        chrome.tabs.sendMessage(
            activeTab.id,

            {
                action: "getJobPageData"
            },

            function(response) {

                if (
                    chrome.runtime.lastError
                ) {

                    console.log(
                        "Error:",
                        chrome.runtime.lastError.message
                    );

                    return;
                }


                if (!response) {

                    console.log(
                        "No response from content script"
                    );

                    return;
                }


                console.log(
                    "Received job data:",
                    response
                );


                document.getElementById(
                    "job-title"
                ).textContent =
                    response.title ||
                    "Not detected";


                document.getElementById(
                    "company"
                ).textContent =
                    response.company ||
                    "Not detected";


                document.getElementById(
                    "location"
                ).textContent =
                    response.location ||
                    "Not detected";


                document.getElementById(
                    "job-url"
                ).textContent =
                    response.url ||
                    "Not detected";
            }
        );
    }
);