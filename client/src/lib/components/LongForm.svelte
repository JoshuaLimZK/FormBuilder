<script>
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    export let datum;
    let titleValue = datum[3]
    let placeholderValue = datum[6]
    let checkboxValue = datum[4]

    function deleteQuestion() {
        const deleteID = datum[0];
        dispatch('delete', deleteID);
    }

    function handleTitleChange(event) {
        titleValue = event.target.value;
    }

    function handlePlaceholderChange(event) {
        placeholderValue = event.target.value;
    }

    function handleInputBlur() {
        const questionID = datum[0];
        const formID = "temp";
        const userID = "temp";
        const questionTitle = titleValue;
        const questionRequired = checkboxValue;
        const questionType = datum[2];
        const questionPlaceholder = placeholderValue;
        const questionData = [questionID, formID, userID, questionTitle, questionRequired, questionType, questionPlaceholder];
        console.log(questionData);
        dispatch('edit', questionData);
    } 

    function handleCheckboxChange(event) {
        checkboxValue = event.target.checked ? 1 : 0;
        handleInputBlur();
    }
</script>

<div class=" w-full mt-3 mb-3" id="{datum[0]}">
    <div class= "w-full flex flex-row align-top">
        <button class=" bg-[url('icons8-delete.svg')] w-7 h-7 bg-no-repeat bg-contain mt-1 mr-1 -translate-x-14" on:click={deleteQuestion}></button>
        <input title="Required?" type="checkbox" class="tooltip -translate-x-14 h-9 w-4 outline-none" bind:checked={checkboxValue} on:change={handleCheckboxChange}>
        <textarea type="text" placeholder="Type a question" class=" w-full outline-none text-2xl h-[32px] resize-none bg-transparent mb-4 font-bold -translate-x-[44.203px]" bind:value={titleValue} on:input={handleTitleChange} on:blur={handleInputBlur}/>
    </div>
    <textarea placeholder="Type placeholder text" class=" outline-none text-n min-h-[120px] w-full resize-none bg-transparent border border-[#D0D0D0] rounded-xl p-3 bg-white shadow-md overflow-y-hidden placeholder-[#D0D0D0]" bind:value={placeholderValue} on:input={handlePlaceholderChange} on:blur={handleInputBlur}/>
</div>