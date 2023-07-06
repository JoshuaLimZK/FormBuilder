<script>
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
       
</script>

<div class="w-screen h-screen flex justify-center bg-[#F8F8F8]">
    <div class=" w-1/2 flex flex-col">
        <div class="h-[150px]"/>
        <textarea type="text" placeholder="Insert form title" class=" outline-none font-bold text-4xl resize-none h-[41px] mb-5 bg-transparent"/>
        <textarea type="text" placeholder="Insert form description" class=" outline-none text-n w-full resize-none bg-transparent mb-7 h-[24px]"/>
        <div class=" w-full">
            <div class= "w-full flex flex-row gap-1 align-top">
                <button class=" bg-[url('icons8-delete.svg')] w-7 h-7 bg-no-repeat bg-contain mt-1 -translate-x-14"></button>
                <input title="Required?" type="checkbox" class="tooltip -translate-x-14 h-9 w-4 outline-none">
                <textarea type="text" placeholder="Type a question" class=" w-full outline-none text-2xl h-[32px] resize-none bg-transparent mb-4 font-bold -translate-x-[3.3rem]"/>
            </div>
            <textarea placeholder="Type placeholder text" class=" outline-none text-n h-[48px] w-full resize-none bg-transparent border border-[#D0D0D0] rounded-xl p-3 bg-white drop-shadow-[0_4px_4px_rgba(174, 174, 174, 0.25)] overflow-y-hidden placeholder-[#D0D0D0]"/>

        </div>
        <button></button>
    </div>
</div>