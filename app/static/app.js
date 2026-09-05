const state = {
  token: localStorage.getItem("bank_demo_token") || "",
  username: localStorage.getItem("bank_demo_username") || "",
  accounts: [],
  transactions: [],
};

const $ = (id) => document.getElementById(id);

function showToast(message, type = "success") {
  const toast = $("toast");
  toast.textContent = message;
  toast.className = `toast show ${type}`;
  window.clearTimeout(showToast.timer);
  showToast.timer = window.setTimeout(() => {
    toast.className = "toast";
  }, 3200);
}

function setBusy(form, busy) {
  const button = form.querySelector('button[type="submit"]');
  if (!button) return;
  button.disabled = busy;
  if (busy) {
    button.dataset.originalText = button.textContent;
    button.textContent = "Processing...";
  } else if (button.dataset.originalText) {
    button.textContent = button.dataset.originalText;
  }
}

async function api(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  if (options.body && !headers["Content-Type"]) headers["Content-Type"] = "application/json";
  if (state.token) headers.Authorization = `Bearer ${state.token}`;

  const response = await fetch(path, { ...options, headers });
  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json") ? await response.json() : await response.text();

  if (response.status === 401 && state.token) {
    logout(false);
  }

  if (!response.ok) {
    const message = payload?.detail || payload || `Request failed with status ${response.status}`;
    throw new Error(typeof message === "string" ? message : JSON.stringify(message));
  }

  return payload;
}

async function checkHealth() {
  const pill = $("apiStatus");
  try {
    const health = await api("/health");
    pill.className = "status-pill online";
    pill.innerHTML = '<span class="status-dot"></span>API Online';
    $("dashboardStatus").textContent = health.status === "ok" ? "Online" : health.status;
  } catch (error) {
    pill.className = "status-pill offline";
    pill.innerHTML = '<span class="status-dot"></span>API Offline';
    $("dashboardStatus").textContent = "Offline";
  }
}

function switchAuthTab(tab) {
  document.querySelectorAll(".auth-tab").forEach((button) => {
    button.classList.toggle("active", button.dataset.authTab === tab);
  });
  $("loginForm").classList.toggle("hidden", tab !== "login");
  $("registerForm").classList.toggle("hidden", tab !== "register");
}

function showDashboard() {
  $("authView").classList.add("hidden");
  $("dashboardView").classList.remove("hidden");
  $("logoutButton").classList.remove("hidden");
  $("welcomeText").textContent = state.username ? `Signed in as ${state.username}` : "Authenticated session";
}

function showAuth() {
  $("dashboardView").classList.add("hidden");
  $("authView").classList.remove("hidden");
  $("logoutButton").classList.add("hidden");
}

function logout(showMessage = true) {
  state.token = "";
  state.username = "";
  state.accounts = [];
  state.transactions = [];
  localStorage.removeItem("bank_demo_token");
  localStorage.removeItem("bank_demo_username");
  showAuth();
  if (showMessage) showToast("Logged out successfully");
}

function money(value, currency = "KES") {
  return new Intl.NumberFormat("en-KE", {
    style: "currency",
    currency,
    minimumFractionDigits: 2,
  }).format(Number(value || 0));
}

function renderAccounts() {
  const grid = $("accountsGrid");
  const empty = $("emptyAccounts");
  grid.innerHTML = "";
  empty.classList.toggle("hidden", state.accounts.length > 0);

  for (const account of state.accounts) {
    const card = document.createElement("article");
    card.className = "account-card";
    card.innerHTML = `
      <span class="account-type">${account.currency} ACCOUNT</span>
      <h3>${escapeHtml(account.account_name)}</h3>
      <div class="account-number">${escapeHtml(account.account_number)}</div>
      <div class="account-balance">${money(account.balance, account.currency)}</div>
    `;
    grid.appendChild(card);
  }

  const kesTotal = state.accounts
    .filter((account) => account.currency === "KES")
    .reduce((sum, account) => sum + Number(account.balance), 0);
  $("totalBalance").textContent = money(kesTotal, "KES");
  $("accountCount").textContent = String(state.accounts.length);

  const options = state.accounts.length
    ? state.accounts.map((account) => `<option value="${escapeHtml(account.account_number)}">${escapeHtml(account.account_name)} · ${escapeHtml(account.account_number)}</option>`).join("")
    : '<option value="">Create an account first</option>';
  $("moneyAccount").innerHTML = options;
  $("transferSource").innerHTML = options;
}

function renderTransactions() {
  const body = $("transactionsBody");
  const empty = $("emptyTransactions");
  body.innerHTML = "";
  empty.classList.toggle("hidden", state.transactions.length > 0);
  $("transactionCount").textContent = String(state.transactions.length);

  for (const tx of state.transactions) {
    const row = document.createElement("tr");
    const isCredit = tx.transaction_type === "DEPOSIT";
    const amountClass = isCredit ? "positive" : "negative";
    const prefix = isCredit ? "+" : "-";
    row.innerHTML = `
      <td><strong>${escapeHtml(tx.reference)}</strong></td>
      <td>${escapeHtml(tx.transaction_type)}</td>
      <td class="amount ${amountClass}">${prefix}${money(tx.amount, "KES")}</td>
      <td><span class="badge ${escapeHtml(String(tx.status).toLowerCase())}">${escapeHtml(tx.status)}</span></td>
      <td>${escapeHtml(tx.description || "—")}</td>
      <td>${new Date(tx.created_at).toLocaleString("en-KE")}</td>
    `;
    body.appendChild(row);
  }
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function loadDashboard() {
  const [accounts, transactions] = await Promise.all([
    api("/accounts"),
    api("/transactions?limit=50"),
  ]);
  state.accounts = accounts;
  state.transactions = transactions;
  renderAccounts();
  renderTransactions();
}

async function login(username, password) {
  const result = await api("/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
  state.token = result.access_token;
  state.username = username;
  localStorage.setItem("bank_demo_token", state.token);
  localStorage.setItem("bank_demo_username", username);
  showDashboard();
  await loadDashboard();
}

document.querySelectorAll(".auth-tab").forEach((button) => {
  button.addEventListener("click", () => switchAuthTab(button.dataset.authTab));
});

$("loginForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  setBusy(event.currentTarget, true);
  try {
    await login($("loginUsername").value.trim(), $("loginPassword").value);
    showToast("Login successful");
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    setBusy(event.currentTarget, false);
  }
});

$("registerForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  setBusy(event.currentTarget, true);
  const username = $("registerUsername").value.trim();
  const password = $("registerPassword").value;
  try {
    await api("/auth/register", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    });
    await login(username, password);
    showToast("User created and logged in");
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    setBusy(event.currentTarget, false);
  }
});

$("logoutButton").addEventListener("click", () => logout());

$("refreshButton").addEventListener("click", async () => {
  try {
    await loadDashboard();
    showToast("Dashboard refreshed");
  } catch (error) {
    showToast(error.message, "error");
  }
});

document.querySelectorAll("[data-open-modal]").forEach((button) => {
  button.addEventListener("click", () => $(button.dataset.openModal).showModal());
});

$("createAccountForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  setBusy(event.currentTarget, true);
  try {
    await api("/accounts", {
      method: "POST",
      body: JSON.stringify({
        account_name: $("accountName").value.trim(),
        opening_balance: $("openingBalance").value,
        currency: $("accountCurrency").value,
      }),
    });
    $("createAccountModal").close();
    event.currentTarget.reset();
    $("openingBalance").value = "0.00";
    await loadDashboard();
    showToast("Account created successfully");
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    setBusy(event.currentTarget, false);
  }
});

$("moneyForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  setBusy(event.currentTarget, true);
  const account = $("moneyAccount").value;
  const operation = $("moneyOperation").value;
  try {
    await api(`/accounts/${encodeURIComponent(account)}/${operation}`, {
      method: "POST",
      body: JSON.stringify({
        amount: $("moneyAmount").value,
        reference: $("moneyReference").value.trim(),
        description: $("moneyDescription").value.trim() || null,
      }),
    });
    event.currentTarget.reset();
    await loadDashboard();
    showToast(`${operation === "deposit" ? "Deposit" : "Withdrawal"} completed`);
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    setBusy(event.currentTarget, false);
  }
});

$("transferForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  setBusy(event.currentTarget, true);
  try {
    await api("/transfers", {
      method: "POST",
      body: JSON.stringify({
        source_account: $("transferSource").value,
        destination_account: $("transferDestination").value.trim(),
        amount: $("transferAmount").value,
        reference: $("transferReference").value.trim(),
        description: $("transferDescription").value.trim() || null,
      }),
    });
    event.currentTarget.reset();
    await loadDashboard();
    showToast("Transfer completed successfully");
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    setBusy(event.currentTarget, false);
  }
});

async function bootstrap() {
  await checkHealth();
  if (!state.token) {
    showAuth();
    return;
  }
  showDashboard();
  try {
    await loadDashboard();
  } catch (error) {
    logout(false);
    showToast("Your session expired. Please log in again.", "error");
  }
}

bootstrap();
window.setInterval(checkHealth, 30000);
