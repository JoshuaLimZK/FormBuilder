<script>
    import { onMount } from "svelte";
    import { page } from "$app/stores";

    let unsubscribe;
    let slug;

    let currentQuestion = 0;

    unsubscribe = page.subscribe((value) => {
        slug = value.params.slug;
    });

    let dataArray = [];
    let componentInstances = [];

    onMount(async () => {
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
    });
</script>

<div class="w-screen flex justify-center">
    <div class=" w-1/2 flex flex-col">
        <div class="h-[150px]" />
        <div class="w-full text-4xl font-bold">Form Title</div>
        <div class="w-full text-xl">Form Description</div>
    </div>
</div>
