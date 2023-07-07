<script>
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    export let datum;
    function deleteQuestion() {
        const deleteID = datum[0];
        dispatch('delete', deleteID);
    }
</script>

<div class=" w-full mt-3 mb-3" id="{datum[0]}">
    <div class= "w-full flex flex-row align-top">
        <button class=" bg-[url('icons8-delete.svg')] w-7 h-7 bg-no-repeat bg-contain mt-1 mr-1 -translate-x-14" on:click={deleteQuestion}></button>
        <input title="Required?" type="checkbox" class="tooltip -translate-x-14 h-9 w-4 outline-none">
        <textarea type="text" placeholder="Type a question" class=" w-full outline-none text-2xl h-[32px] resize-none bg-transparent mb-4 font-bold -translate-x-[44.203px]"/>
    </div>
    <textarea placeholder="Type placeholder text" class=" outline-none text-n min-h-[120px] w-full resize-none bg-transparent border border-[#D0D0D0] rounded-xl p-3 bg-white shadow-md overflow-y-hidden placeholder-[#D0D0D0]"/>
</div>