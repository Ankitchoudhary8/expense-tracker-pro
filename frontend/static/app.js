const form = document.querySelector("#expense-form");
const list = document.querySelector("#expenses");
const total = document.querySelector("#total");
const message = document.querySelector("#message");
const dateInput = document.querySelector("#date");
dateInput.value = new Date().toLocaleDateString("en-CA");
const money = value => new Intl.NumberFormat("en-IN", {style:"currency",currency:"INR"}).format(value);

async function loadExpenses() {
  try {
    const response = await fetch("/api/expenses");
    if (!response.ok) throw new Error("Could not load expenses.");
    const expenses = await response.json();
    total.textContent = money(expenses.reduce((sum, item) => sum + item.amount, 0));
    list.replaceChildren();
    if (!expenses.length) {
      const empty = document.createElement("p");
      empty.className = "empty";
      empty.textContent = "No expenses yet. Add your first expense!";
      list.append(empty);
    }
    expenses.forEach(item => {
      const row = document.createElement("div");
      row.className = "expense";
      const info = document.createElement("div");
      const name = document.createElement("strong");
      name.textContent = item.title;
      const detail = document.createElement("small");
      detail.textContent = item.category + " • " + item.date;
      info.append(name, detail);
      const right = document.createElement("div");
      right.className = "right";
      const amount = document.createElement("strong");
      amount.textContent = money(item.amount);
      const button = document.createElement("button");
      button.className = "delete";
      button.textContent = "Delete";
      button.addEventListener("click", () => removeExpense(item.id));
      right.append(amount, button);
      row.append(info, right);
      list.append(row);
    });
  } catch (error) { message.textContent = error.message; }
}

async function removeExpense(id) {
  try {
    const response = await fetch("/api/expenses/" + id, {method:"DELETE"});
    if (!response.ok) throw new Error("Could not delete expense.");
    message.textContent = "";
    await loadExpenses();
  } catch (error) { message.textContent = error.message; }
}

form.addEventListener("submit", async event => {
  event.preventDefault();
  message.textContent = "";
  const payload = {
    title: document.querySelector("#title").value.trim(),
    amount: Number(document.querySelector("#amount").value),
    category: document.querySelector("#category").value,
    date: dateInput.value
  };
  try {
    const response = await fetch("/api/expenses", {
      method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload)
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Could not add expense.");
    form.reset();
    dateInput.value = new Date().toLocaleDateString("en-CA");
    await loadExpenses();
  } catch (error) { message.textContent = error.message; }
});
loadExpenses();
