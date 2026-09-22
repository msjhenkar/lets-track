console.log("Job Tracker content script loaded");


function extractJobData() {

    const jobData = {
        title: null,
        company: null,
        location: null,
        description: null,
        url: window.location.href
    };


    // ==========================================
    // 1. Applied Materials - Job Title
    // ==========================================

    const appliedMaterialsTitle =
        document.querySelector("[class*='position-title']");

    if (appliedMaterialsTitle) {
        jobData.title =
            appliedMaterialsTitle.innerText.trim();
    }


    // ==========================================
    // 2. Generic H1 fallback
    // ==========================================

    if (!jobData.title) {

        const h1 = document.querySelector("h1");

        if (h1) {
            jobData.title =
                h1.innerText.trim();
        }
    }


    // ==========================================
    // 3. OpenGraph fallback
    // ==========================================

    if (!jobData.title) {

        const ogTitle =
            document.querySelector(
                'meta[property="og:title"]'
            );

        if (ogTitle) {
            jobData.title =
                ogTitle.content.trim();
        }
    }


    // ==========================================
    // 4. JSON-LD
    // ==========================================

    const jsonLdScripts =
        document.querySelectorAll(
            'script[type="application/ld+json"]'
        );


    for (const script of jsonLdScripts) {

        try {

            const data =
                JSON.parse(script.textContent);

            const items =
                Array.isArray(data)
                    ? data
                    : [data];


            for (const item of items) {

                if (item["@type"] === "JobPosting") {

                    // Only use JSON-LD title if
                    // we don't already have one
                    if (!jobData.title) {
                        jobData.title =
                            item.title || null;
                    }


                    if (
                        !jobData.company &&
                        item.hiringOrganization
                    ) {

                        jobData.company =
                            item.hiringOrganization.name ||
                            null;
                    }


                    if (!jobData.description) {

                        jobData.description =
                            item.description || null;
                    }


                    if (
                        !jobData.location &&
                        item.jobLocation
                    ) {

                        const location =
                            item.jobLocation;


                        if (location.address) {

                            jobData.location =
                                location.address
                                    .addressLocality ||
                                null;
                        }
                    }
                }
            }

        } catch (error) {

            console.log(
                "Could not parse JSON-LD:",
                error
            );
        }
    }


    // ==========================================
    // 5. Applied Materials company fallback
    // ==========================================

    if (
        !jobData.company &&
        window.location.hostname.includes(
            "appliedmaterials.com"
        )
    ) {

        jobData.company =
            "Applied Materials";
    }


    // ==========================================
    // 6. Debug output
    // ==========================================

    console.log(
        "========== JOB TRACKER =========="
    );

    console.log(
        "Extracted Job Data:",
        jobData
    );

    console.log(
        "Job Title:",
        jobData.title
    );

    console.log(
        "Company:",
        jobData.company
    );

    console.log(
        "Location:",
        jobData.location
    );

    console.log(
        "Description:",
        jobData.description
    );

    console.log(
        "URL:",
        jobData.url
    );

    console.log(
        "================================"
    );


    return jobData;
}


// ==========================================
// Message listener
// ==========================================

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {

        if (
            request.action ===
            "getJobPageData"
        ) {

            const jobData =
                extractJobData();

            sendResponse(jobData);
        }
    }
);