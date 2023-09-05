<script>
    let username;
    let password;
    async function submit() {
        const response = await fetch("http://localhost:6969/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                data: [username, password],
            }),
        });

        const error = await response.json();
        if (error["Error"] === "That Username does not Exist") {
            alert("That Username does not Exist");
        } else if (error["Error"] === "Incorrect Password") {
            alert("Incorrect Password");
        } else {
            document.cookie = "uuid=" + error["uuid"];
            window.location.href = "/dashboard";
        }
    }
</script>

<div
    class=" h-screen w-full font-semibold text-3xl flex items-center justify-center flex-col gap-5"
>
    Log In
    <div class=" grid grid-cols-2 grid-rows-3 text-xl font-normal gap-3">
        <div class="flex items-center">Username:</div>
        <div><input class="p-2 rounded-lg" bind:value={username} /></div>
        <div class="flex items-center">Password</div>
        <div>
            <input
                class="p-2 rounded-lg"
                bind:value={password}
                type="password"
            />
        </div>
    </div>
    <button
        class="text-lg border-2 rounded-lg bg-white w-[100px] h-[50px]"
        on:click={submit}>Log In</button
    >
</div>
