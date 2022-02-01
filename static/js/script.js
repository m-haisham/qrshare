// tippy
document.querySelectorAll("[data-tippy]").forEach((element) => {
    const target = document.querySelector(element.getAttribute("href"));
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

// tooltip
document.querySelectorAll("[tooltip]").forEach((element) => {
    const tooltip = element.getAttribute("tooltip").trim();
    if (tooltip == null) {
        return;
    }

    tippy(element, {
        content: tooltip,
        theme: "light",
        placement: element.dataset.placement,
    });
});
