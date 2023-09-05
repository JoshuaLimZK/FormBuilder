<div class="w-full h-screen flex justify-center items-center flex-col gap-5">
    <div class="font-semibold text-4xl">Start making forms now!</div>
    <div class="flex flex-row gap-5">
        <button
            class="text-lg border-2 rounded-lg bg-white w-[100px] h-[50px]"
            on:click={() => (window.location.href = "/signup")}>Sign Up</button
        >
        <button
            class="text-lg border-2 rounded-lg bg-white w-[100px] h-[50px]"
            on:click={() => (window.location.href = "/login")}>Log In</button
        >
    </div>
</div>
