// tippy
document.querySelectorAll("[data-tippy]").forEach((element) => {
    const target = document.querySelector(element.getAttribute("href"));
    console.log({ element, target });
    if (target == null) {
        return;
    }

    target.style.display = element.dataset.display ?? "block";
    tippy(element, {
        content: target,
        theme: "light",
        trigger: "click",
    });
});
