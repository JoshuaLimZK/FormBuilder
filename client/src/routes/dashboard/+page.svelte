<script>
    import { onMount } from "svelte";

    let listOfForms = [];
    let username = "";

    onMount(async () => {
        let cookies = document.cookie;
        try {
            let response = await fetch("http://127.0.0.1:6969/getForm", {
                method: "POST",
                body: JSON.stringify({ userID: cookies.split("=")[1] }),
            });
            const receivedData = await response.json();
            listOfForms = receivedData["data"];
        } catch (err) {
            console.log(err);
        }

        try {
            let response = await fetch("http://127.0.0.1:6969/getUsername", {
                method: "POST",
                body: JSON.stringify({ userID: cookies.split("=")[1] }),
            });
            const receivedData = await response.json();
            username = receivedData["data"][0][1];
        } catch (err) {
            console.log(err);
            window.location.href = "/";
        }
    });

    function handleClick(url) {
        window.location.href = "/editor/" + url;
    }

    async function addForm() {
        let cookies = document.cookie;
        let newUUID = crypto.randomUUID();
        let newDate = new Date().toLocaleDateString("en-GB");
        try {
            await fetch("http://127.0.0.1:6969/newForm", {
                method: "POST",
                body: JSON.stringify({
                    data: [newUUID, cookies.split("=")[1], "", newDate, ""],
                }),
            });
            window.location.href = "/editor/" + newUUID;
        } catch (err) {
            console.log(err);
        }
    }
</script>

<div class=" sticky top-0 h-20 border-b border-[#D0D0D0] bg-white" />
<div class="w-full flex justify-center bg-[#F1F1F1]">
    <div class="w-1/2 h-screen flex flex-col">
        <h1 class=" mt-16 font-bold text-4xl mb-6">{username}'s Forms</h1>
        {#if listOfForms.length != 0}
            {#each listOfForms as form}
                <button
                    class="hover:bg-[#E5E5E5] pt-3 pb-3 pl-5 mt-2 mb-2 flex flex-col rounded-lg"
                    on:click={() => handleClick(form[0])}
                >
                    <b class="text-lg">{form[2]}</b>
                    Created on {form[3]}
                </button>
            {/each}
        {:else}
            <p class="text-lg">You have no forms yet.</p>
        {/if}
        <div class="w-full flex justify-center">
            <button
                class=" mt-10 w-9 h-9 bg-white border border-[#D0D0D0] rounded-lg drop-shadow-[0_4px_4px_rgba(174, 174, 174, 0.25)] bg-[url('/icons8-plus-96.png')] bg-contain bg-no-repeat shadow-md hover:shadow-lg"
                on:click={addForm}
            />
        </div>
    </div>
</div>
