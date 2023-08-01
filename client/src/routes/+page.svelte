<script>
    import { onMount } from "svelte";

    let listOfForms = [];
    let username = "";

    onMount(async () => {
        try {
            let response = await fetch("http://localhost:6969/getForm", {
                method: "POST",
                body: JSON.stringify({ userID: "temp" }),
            });
            const receivedData = await response.json();
            listOfForms = receivedData["data"];
        } catch (err) {
            console.log(err);
        }

        try {
            let response = await fetch("http://localhost:6969/getUsername", {
                method: "POST",
                body: JSON.stringify({ userID: "temp" }),
            });
            const receivedData = await response.json();
            username = receivedData["data"][0][1];
        } catch (err) {
            console.log(err);
        }
    });

    function handleClick(url) {
        window.location.href = "/editor/" + url;
    }
</script>

<div class=" sticky top-0 h-20 border-b border-[#D0D0D0] bg-white" />
<div class="w-full flex justify-center bg-[#F8F8F8]">
    <div class="w-1/2 h-screen flex flex-col">
        <h1 class=" mt-16 font-bold text-4xl mb-6">{username}'s Forms</h1>
        {#if listOfForms.length != 0}
            {#each listOfForms as form}
                <button
                    class="hover:bg-[#E5E5E5] pt-3 pb-3 pl-5 mt-2 mb-2 flex flex-col rounded-lg"
                    on:click={() => handleClick(form[0])}
                >
                    <b class="text-lg">{form[2]}</b>
                    Edited 10 minutes ago
                </button>
            {/each}
        {:else}
            <p class="text-lg">You have no forms yet.</p>
        {/if}
    </div>
</div>
