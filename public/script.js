const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");
const products = document.querySelectorAll(".product");
const dynamicMessage = document.getElementById("dynamic-message");

// Palavras que indicam encerramento do chat
const closeChatKeywords = ["sair", "encerrar", "fechar", "finalizar", "fim", "encerrado"];

// Variável para o temporizador de inatividade
let inactivityTimer;

// Variável para armazenar o produto selecionado
let selectedProduct = null;

// Função para limpar o chat box
function clearChatBox() {
    chatBox.innerHTML = "";
}

// Atualiza a mensagem dinâmica no menu lateral
function updateDynamicMessage(productName) {
    dynamicMessage.textContent = `Iniciado atendimento sobre ${productName}`;
}

// Adiciona a mensagem inicial de orientação
function showInitialMessage() {
    clearChatBox();
    const initialMessage = "Bem-vindo! Selecione um dos produtos ou faça uma pergunta para começar.";
    const messageElement = document.createElement("div");
    messageElement.classList.add("center-message");
    messageElement.textContent = initialMessage;
    chatBox.appendChild(messageElement);
}

// Exibe a mensagem inicial ao carregar a página
document.addEventListener("DOMContentLoaded", () => {
    showInitialMessage();
});

// Lida com o clique em um produto
products.forEach(product => {
    product.addEventListener("click", () => {
        selectedProduct = product.dataset.product;

        // Reativa o campo de entrada e botão de envio
        userInput.disabled = false;
        sendButton.disabled = false;

        // Limpa o campo de entrada
        userInput.value = "";

        // Atualiza a mensagem dinâmica no menu lateral
        updateDynamicMessage(selectedProduct);

        // Limpa o chat para iniciar novo atendimento
        clearChatBox();

        // Reinicia o temporizador de inatividade
        resetInactivityTimer();

        // Adiciona mensagem inicial do produto no chat
        addMessageToChatBox(`Você está consultando informações sobre o produto: ${selectedProduct}`, "bot-message");
    });
});

// Função para encerrar o chat
function closeChat(reason = "O chat foi encerrado. Obrigado por utilizar nosso atendimento!") {
    clearChatBox(); // Limpa o chat
    dynamicMessage.textContent = reason;
    userInput.disabled = true; // Desativa o campo de entrada
    sendButton.disabled = true; // Desativa o botão de envio
    userInput.value = ""; // Limpa o campo de entrada
    clearTimeout(inactivityTimer); // Cancela o temporizador de inatividade
}

// Função para formatar o horário atual (hh:mm)
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

// Função para adicionar mensagens ao chat box
function addMessageToChatBox(message, className) {
    const container = document.createElement("div");
    container.classList.add("message-container", className);

    const messageElement = document.createElement("div");
    messageElement.classList.add("message");
    messageElement.textContent = message;

    const timeElement = document.createElement("div");
    timeElement.classList.add("message-time");
    timeElement.textContent = getCurrentTime();

    container.appendChild(messageElement);
    container.appendChild(timeElement);
    chatBox.appendChild(container);

    chatBox.scrollTop = chatBox.scrollHeight;
}

// Função para enviar mensagens
async function sendMessage() {
    const question = userInput.value.trim();
    if (!question) return;

    if (!selectedProduct) {
        addMessageToChatBox("Por favor, selecione um produto antes de enviar sua pergunta.", "bot-message");
        return;
    }

    // Verifica se o usuário deseja encerrar o chat
    if (closeChatKeywords.some(keyword => question.toLowerCase().includes(keyword))) {
        closeChat();
        return;
    }

    // Adiciona a mensagem do usuário ao chat
    addMessageToChatBox(question, "user-message");

    // Limpa o campo de entrada após envio
    userInput.value = "";

    // Reinicia o temporizador de inatividade
    resetInactivityTimer();

    try {
                    const response = await fetch("https://chatbot-knolojji.onrender.com/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question, product: selectedProduct })
        });
        const data = await response.json();

        // Adiciona a resposta do bot ao chat
        addMessageToChatBox(data.answer, "bot-message");
    } catch (error) {
        console.error("Erro ao se comunicar com o servidor:", error);
        addMessageToChatBox("Erro ao se comunicar com o servidor. Tente novamente mais tarde.", "bot-message");
    }
}

// Função para reiniciar o temporizador de inatividade
function resetInactivityTimer() {
    clearTimeout(inactivityTimer); // Cancela o temporizador anterior, se houver
    inactivityTimer = setTimeout(() => {
        closeChat("O chat foi encerrado por inatividade.");
    }, 5 * 60 * 1000); // 5 minutos de inatividade
}

// Eventos de clique e tecla Enter
sendButton.addEventListener("click", sendMessage);
userInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});
