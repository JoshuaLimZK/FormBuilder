<script>
    import LongForm from "../lib/components/LongForm.svelte";
    
    import { onMount } from "svelte";

    let dataArray = [];
    let componentInstances = [];

    async function addQuestion() {
        const response = await fetch('http://localhost:6969/createQuestion', {
            method: 'POST',
            body: JSON.stringify({questionType: 0})
        })
        const receivedData = await response.json();
        dataArray = [...dataArray, receivedData["data"]];
        componentInstances = dataArray.map(datum => ({id: datum[0], data: datum}))
    }

    async function editQuestion(event) {
        const response = await fetch('http://localhost:6969/editQuestion', {
            method: "POST",
            body: JSON.stringify({data: event.detail})
        })
    }

    async function deleteQuestion(event) {
        const response = await fetch('http://localhost:6969/deleteQuestion', {
            method: "POST",
            body: JSON.stringify({questionID: event.detail, formID: "temp"})
        })
        const receivedData = await response.json();
        console.log(receivedData)
        dataArray = receivedData["data"];
        componentInstances = dataArray.map(datum => ({id: datum[0], data: datum}))
    }

    onMount(async () => {
        try {
            let response = await fetch(`http://localhost:6969/getData?form=${"temp"}`);
            const receivedData = await response.json();
            dataArray = receivedData["data"];
            componentInstances = dataArray.map(datum => ({id: datum[0], data: datum}))
        } catch (err) {
            console.log(err);
        }


        const tx = document.getElementsByTagName("textarea");
        for (let i = 0; i < tx.length; i++) {
            tx[i].setAttribute("style", "height:" + (tx[i].scrollHeight) + "px;overflow-y:hidden;");
            tx[i].addEventListener("input", OnInput, false);
        }

        function OnInput() {
            this.style.height = 0;
            this.style.height = (this.scrollHeight) + "px";
        }


    });
</script>

<div class="w-screen flex justify-center">
    <div class=" w-1/2 flex flex-col">
        <div class="h-[150px]"/>
        <textarea type="text" placeholder="Insert form title" class=" outline-none font-bold text-4xl resize-none h-[41px] mb-5 bg-transparent"/>
        <textarea type="text" placeholder="Insert form description" class=" outline-none text-n w-full resize-none bg-transparent mb-7 h-[24px]"/>
        {#if dataArray === []}
            Loading...
        {:else}
            {#each componentInstances as instance (instance.id)}
                <svelte:component this={LongForm} datum={instance.data} on:delete={deleteQuestion} on:edit={editQuestion}/>
            {/each}
        {/if}
        <div class="w-full flex justify-center">
            <button class=" mt-10 w-9 h-9 bg-white border border-[#D0D0D0] rounded-lg drop-shadow-[0_4px_4px_rgba(174, 174, 174, 0.25)] bg-[url(icons8-plus-96.png)] bg-contain bg-no-repeat shadow-md" on:click={addQuestion}/>
        </div>
    </div>
</div>