<script>
    import LongForm from "../../../lib/components/LongForm.svelte";

    import { onMount } from "svelte";

    import { page } from "$app/stores";

    import { goto } from "$app/navigation";
    import Layout from "../../+layout.svelte";

    let unsubscribe;
    let slug;

    let titleValue = "";
    let descriptionValue = "";

    unsubscribe = page.subscribe((value) => {
        slug = value.params.slug;
    });

    let dataArray = [];
    let componentInstances = [];

    async function addQuestion() {
        const response = await fetch("http://localhost:6969/createQuestion", {
            method: "POST",
            body: JSON.stringify({ formUUID: slug, questionType: 0 }),
        });
        const receivedData = await response.json();
        dataArray = [...dataArray, receivedData["data"]];
        componentInstances = dataArray.map((datum) => ({
            id: datum[0],
            data: datum,
        }));
    }

    async function editQuestion(event) {
        const response = await fetch("http://localhost:6969/editQuestion", {
            method: "POST",
            body: JSON.stringify({ data: event.detail }),
        });
    }

    async function editFormInfo(event) {
        const response = await fetch("http://localhost:6969/editFormInfo", {
            method: "POST",
            body: JSON.stringify({
                data: [titleValue, descriptionValue, slug],
            }),
        });
    }

    async function deleteQuestion(event) {
        const response = await fetch("http://localhost:6969/deleteQuestion", {
            method: "POST",
            body: JSON.stringify({ questionID: event.detail, formID: slug }),
        });
        const receivedData = await response.json();
        console.log(receivedData);
        dataArray = receivedData["data"];
        componentInstances = dataArray.map((datum) => ({
            id: datum[0],
            data: datum,
        }));
    }

    let cookies = null;
    let userUUID = "";

    onMount(async () => {
        cookies = document.cookie;
        try {
            let response = await fetch(
                `http://localhost:6969/getData?form=${slug}`
            );
            const receivedData = await response.json();
            dataArray = receivedData["data"];
            componentInstances = dataArray.map((datum) => ({
                id: datum[0],
                data: datum,
            }));
        } catch (err) {
            console.log(err);
        }

        try {
            let response = await fetch(
                `http://localhost:6969/getFormInfo?form=${slug}`
            );
            const receivedData = await response.json();

            userUUID = receivedData["data"][0][2];

            titleValue = receivedData["data"][0][0];

            descriptionValue = receivedData["data"][0][1];
        } catch (err) {
            console.log(err);
        }

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

    function backRedirect() {
        window.location.href = "/dashboard";
    }
</script>

<div
    class=" sticky top-0 h-20 border-b border-[#D0D0D0] bg-white flex flex-row"
>
    <div class="w-1/2 flex justify-start items-center ml-10">
        <button
            class="bg-[url('/icons8-back-50.png')] w-7 h-7 bg-no-repeat bg-contain hover:-translate-x-2 transition duration-500 ease-in-out"
            on:click={backRedirect}
        />
    </div>
    <div class="w-1/2 flex justify-end items-center mr-10">
        <button
            class="bg-[url('/icons8-link-50.png')] w-7 h-7 bg-no-repeat bg-contain hover:rotate-180 transition duration-500 ease-in-out"
            on:click={(window.location.href = "/form/" + slug)}
        />
    </div>
</div>
<div class="w-full flex justify-center bg-[#F1F1F1] h-full">
    {#if cookies === null}
        loading...
    {:else if cookies.split("=")[1] === userUUID}
        <div class="w-screen flex justify-center">
            <div class=" w-1/2 flex flex-col">
                <div class="h-[150px]" />
                <textarea
                    id="textarea"
                    type="text"
                    placeholder="Insert form title"
                    class=" outline-none font-bold text-4xl resize-none h-[41px] mb-5 bg-transparent overflow-y-hidden"
                    bind:value={titleValue}
                    on:blur={editFormInfo}
                />
                <textarea
                    id="textarea"
                    type="text"
                    placeholder="Insert form description"
                    class=" outline-none text-n w-full resize-none bg-transparent mb-7 h-[24px]"
                    bind:value={descriptionValue}
                    on:blur={editFormInfo}
                />
                {#if dataArray === []}
                    Loading...
                {:else}
                    {#each componentInstances as instance (instance.id)}
                        <svelte:component
                            this={LongForm}
                            datum={instance.data}
                            {slug}
                            on:delete={deleteQuestion}
                            on:edit={editQuestion}
                        />
                    {/each}
                {/if}
                <div class="w-full flex justify-center">
                    <button
                        class=" mt-10 w-9 h-9 bg-white border border-[#D0D0D0] rounded-lg drop-shadow-[0_4px_4px_rgba(174, 174, 174, 0.25)] bg-[url('/icons8-plus-96.png')] bg-contain bg-no-repeat shadow-md hover:shadow-lg"
                        on:click={addQuestion}
                    />
                </div>
            </div>
        </div>
    {:else}
        You are not authorised to edit this form.
    {/if}
</div>
