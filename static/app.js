

    const darkButton = document.getElementById("darkModeBtn");

    darkButton.onclick = function(){
    document.body.classList.toggle("dark");
    };

    const form = document.getElementById("askForm");
    const button = document.getElementById("askButton");
    const loading = document.getElementById("loading")
    form.addEventListener("submit", function(){

    button.disabled = true;
    button.textContent = "Generating...";
    loading.style.display = "block";
    });
    
    
    const textarea = document.getElementById("questionBox");
    const counter = document.getElementById("counter");
    textarea.addEventListener("input", function(){
    counter.textContent = textarea.value.length;
    });
    

    
    function copyResponse(){
    let text =
    document.getElementById("aiResponse").innerText;
    navigator.clipboard.writeText(text);
    alert("Response copied!");
    }
    

    
    function showLoading(){
    document.getElementById("loading")
    .style.display="block";
    }



    const text = "Hi! I am your AI assistant. What are we working on today?";

    let index = 0;

    function typePlaceholder(){

    if(index < text.length){

        textarea.placeholder += text.charAt(index);
        index++;

        setTimeout(typePlaceholder, 80);
    }

}

typePlaceholder();

function toggleanswer(id) {
    const answer = document.getElementById("answer-" + id);
    if (answer.style.display === "block") {
        answer.style.display = "none";

    } else {
        answer.style.display ="block";
    }
}