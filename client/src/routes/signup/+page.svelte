<script>
    let username;
    let password;
    let confirmPassword;
    async function submit() {
        if (password !== confirmPassword) {
            alert("Passwords do not match");
            return;
        }
        const response = await fetch("http://localhost:6969/signUp", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                data: [username, password],
            }),
        });

        const error = await response.json();
        if (error["Error"] === "That Username is Already Taken") {
            alert("That Username is Already Taken");
        } else {
            window.location.href = "/login";
        }
    }
</script>

<div
    class=" h-screen w-full font-semibold text-3xl flex items-center justify-center flex-col gap-5"
>
    Sign Up
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
        <div class="flex items-center">Confirm Password:</div>
        <div>
            <input
                class="p-2 rounded-lg"
                bind:value={confirmPassword}
                type="password"
            />
        </div>
    </div>
    <button
        class="text-lg border-2 rounded-lg bg-white w-[100px] h-[50px]"
        on:click={submit}>Submit</button
    >
</div>
