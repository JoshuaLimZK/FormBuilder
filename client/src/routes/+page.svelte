<script>
    import LongForm from "../lib/components/LongForm.svelte";
    
    import { onMount } from "svelte";
    onMount(() => {
        const tx = document.getElementsByTagName("textarea");
        for (let i = 0; i < tx.length; i++) {
            tx[i].setAttribute("style", "height:" + (tx[i].scrollHeight) + "px;overflow-y:hidden;");
            tx[i].addEventListener("input", OnInput, false);
        }

        function OnInput() {
            this.style.height = 0;
            this.style.height = (this.scrollHeight) + "px";
        }

    })

    async function addQuestion() {
        const response = await fetch('http://localhost:6969/createQuestion', {
            method: 'POST',
            body: JSON.stringify({userUUID: "test", formUUID: "test", selfUUID: "test", questionTitle: "test", isRequired: 1})
        })
        console.log("works")
    }

</script>

<div class="w-screen h-screen flex justify-center bg-[#F8F8F8]">
    <div class=" w-1/2 flex flex-col">
        <div class="h-[150px]"/>
        <textarea type="text" placeholder="Insert form title" class=" outline-none font-bold text-4xl resize-none h-[41px] mb-5 bg-transparent"/>
        <textarea type="text" placeholder="Insert form description" class=" outline-none text-n w-full resize-none bg-transparent mb-7 h-[24px]"/>
        {#each {length: 3} as _, i}
            <svelte:component this={LongForm} />
        {/each}
        <div class="w-full flex justify-center">
            <button class=" mt-10 w-9 h-9 bg-white border border-[#D0D0D0] rounded-lg drop-shadow-[0_4px_4px_rgba(174, 174, 174, 0.25)] bg-[url(icons8-plus-96.png)] bg-contain bg-no-repeat shadow-md" on:click={addQuestion}/>
        </div>
    </div>
</div>