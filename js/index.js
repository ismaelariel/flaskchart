window.onload = function () {
    const handlerStateMachine = document.querySelector(".div_button_content_part_large");

    handlerStateMachine.addEventListener("click", function () {
        window.location.href = "/state";
    }, false);
};
