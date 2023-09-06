<script>
    import { onMount, beforeUpdate } from "svelte";
    import { page } from "$app/stores";

    let unsubscribe;
    let slug;

    let currentQuestion = 0;
    let responseUUID = crypto.randomUUID();

    let titleValue = "";
    let descriptionValue = "";

    let submitted = false;

    unsubscribe = page.subscribe((value) => {
        slug = value.params.slug;
    });

    let dataArray = [];

    let responseArray = [];

    onMount(async () => {
        try {
            let response = await fetch(
                `http://127.0.0.1:6969/getData?form=${slug}`
            );
            const receivedData = await response.json();
            dataArray = receivedData["data"];
            console.log();
        } catch (err) {
            console.log(err);
        }

        try {
            let response = await fetch(
                `http://127.0.0.1:6969/getFormInfo?form=${slug}`
            );
            const receivedData = await response.json();
            titleValue = receivedData["data"][0][0];
            descriptionValue = receivedData["data"][0][1];
        } catch (err) {
            console.log(err);
        }

        const tx = document.getElementsByTagName("textarea");
        for (let i = 0; i < tx.length; i++) {
            tx[i].setAttribute(
                "style",
                "height:" + tx[i].scrollHeight + "px;overflow-y:hidden;"
            );
            tx[i].addEventListener("input", OnInput, false);
        }

        function OnInput() {
            this.style.height = 0;
            this.style.height = this.scrollHeight + "px";
        }

        for (let i = 0; i < dataArray.length; i++) {
            responseArray.push([
                responseUUID,
                dataArray[i][1],
                dataArray[i][0],
                "",
            ]);
        }
    });

    function nextQuestion() {
        currentQuestion++;
    }

    function previousQuestion() {
        currentQuestion--;
    }

    function submitResponse() {
        for (let i = 0; i < responseArray.length; i++) {
            if (dataArray[i][4] === 1 && responseArray[i][3] === "") {
                alert("Please fill in all required fields");
                return;
            }
        }

        try {
            fetch("http://127.0.0.1:6969/submitResponse", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    data: responseArray,
                }),
            });

            submitted = true;
        } catch (err) {
            console.log(err);
        }
    }

    beforeUpdate(() => {
        const tx = document.getElementsByTagName("Textarea");
        for (let i = 0; i < tx.length; i++) {
            tx[i].setAttribute("style", "height:" + tx[i].scrollHeight + "px;");
            tx[i].addEventListener("input", OnInput, false);
        }

        function OnInput() {
            this.style.height = 0;
            this.style.height = this.scrollHeight + "px";
        }
    });
</script>

<div class="w-full flex justify-center bg-[#F1F1F1] h-full">
    <div class="w-screen flex justify-center">
        <div class=" w-1/2 flex flex-col">
            {#if submitted}
                <div class="w-full h-full flex justify-center align-middle">
                    Thank you for your response
                </div>
            {:else}
                <div class="h-[150px]" />
                <div class="w-full text-5xl font-bold mb-5">{titleValue}</div>
                <div class="w-full text-xl mb-20">{descriptionValue}</div>

                {#if dataArray.length === 0 || responseArray.length === 0}
                    This form has no questions or no title, Please contact the
                    creator of this form if there are any issues.
                {:else}
                    <div
                        class="text-xl font-bold mb-4 flex flex-row items-center gap-3"
                    >
                        {dataArray[currentQuestion][3]}
                        {#if dataArray[currentQuestion][4] === 1}
                            <div
                                class=" bg-white border-[#D0D0D0] border h-5 w-5 rounded-md flex justify-center align-middle"
                            >
                                <div class="-translate-y-[1px]">*</div>
                            </div>
                        {/if}
                    </div>
                    <textarea
                        placeholder={dataArray[currentQuestion][6]}
                        class=" outline-none text-n min-h-[120px] w-full resize-none bg-transparent border border-[#D0D0D0] rounded-lg p-3 bg-white shadow-md hover:shadow-lg overflow-y-hidden placeholder-[#D0D0D0]"
                        bind:value={responseArray[currentQuestion][3]}
                    />
                    <div class="w-full flex flex-row gap-2 mt-4">
                        {#if currentQuestion != 0}
                            {#if currentQuestion === dataArray.length - 1}
                                <button
                                    class="bg-black text-white font-bold pr-3 pl-3 pt-1 pb-1 rounded-lg"
                                    on:click={previousQuestion}
                                >
                                    ← Back
                                </button>
                                <button
                                    class="bg-black text-white font-bold pr-3 pl-3 pt-1 pb-1 rounded-lg"
                                    on:click={submitResponse}
                                >
                                    Submit
                                </button>
                            {:else}
                                <button
                                    class="bg-black text-white font-bold pr-3 pl-3 pt-1 pb-1 rounded-lg"
                                    on:click={previousQuestion}
                                >
                                    ← Back
                                </button>
                                <button
                                    class="bg-black text-white font-bold pr-3 pl-3 pt-1 pb-1 rounded-lg"
                                    on:click={nextQuestion}
                                >
                                    Next →
                                </button>
                            {/if}
                        {:else}
                            <button
                                class="bg-black text-white font-bold pr-3 pl-3 pt-1 pb-1 rounded-lg"
                                on:click={nextQuestion}
                            >
                                Next →
                            </button>
                        {/if}
                    </div>
                {/if}
            {/if}
        </div>
    </div>
</div>
