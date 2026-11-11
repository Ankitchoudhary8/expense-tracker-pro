const $ = selector => document.querySelector(selector);
const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
const secureFetch = (url, options = {}) => fetch(url, {
  ...options,
  headers: {...(options.headers || {}), "X-CSRF-Token": csrfToken}
});
const money = value => new Intl.NumberFormat("en-IN", {style:"currency", currency:"INR", maximumFractionDigits:2}).format(value);
const compact = value => new Intl.NumberFormat("en-IN", {notation:"compact", maximumFractionDigits:1}).format(value);
const palette = ["#3657b7","#5f82e8","#25a69a","#f4aa4a","#8b65ce","#e67d89"];
const categories = ["Food","Transport","Shopping","Bills","Education","Other"];
let allExpenses = [];
let editingId = null;
let activeBudget = null;
const localToday = () => {const d = new Date(); return [d.getFullYear(),String(d.getMonth()+1).padStart(2,"0"),String(d.getDate()).padStart(2,"0")].join("-");};
$("#date").value = localToday();
$("#month-filter").value = localToday().slice(0,7);

function filteredExpenses() {
  const month = $("#month-filter").value;
  const category = $("#category-filter").value;
  return allExpenses.filter(item => (!month || item.date.startsWith(month)) && (!category || item.category === category));
}
function drawCategoryChart(items) {
  const totals = categories.map((category,i) => ({category,color:palette[i],amount:items.filter(x=>x.category===category).reduce((sum,x)=>sum+x.amount,0)})).filter(x=>x.amount>0);
  const grand = totals.reduce((sum,x)=>sum+x.amount,0);
  let offset = 0;
  const stops = totals.map(x => {const start=offset;offset+=x.amount/grand*100;return x.color+" "+start+"% "+offset+"%";});
  $("#donut").style.background = stops.length ? "conic-gradient("+stops.join(",")+")" : "#e7ebf4";
  $("#donut").setAttribute("aria-label",totals.length ? totals.map(x=>x.category+": "+money(x.amount)).join(", ") : "No spending");
  $("#donut-total").textContent = money(grand);
  $("#legend").replaceChildren();
  if(!totals.length){const p=document.createElement("p");p.className="empty";p.textContent="No expenses for this selection.";$("#legend").append(p);}
  totals.forEach(x=>{
    const row=document.createElement("div");row.className="legend-row";
    const name=document.createElement("span");name.className="legend-name";
    const swatch=document.createElement("span");swatch.className="swatch";swatch.style.background=x.color;
    name.append(swatch,document.createTextNode(x.category));
    const value=document.createElement("strong");value.textContent=Math.round(x.amount/grand*100)+"%";
    row.append(name,value);$("#legend").append(row);
  });
}
function drawMonthlyChart() {
  const selected = $("#month-filter").value;
  const anchor = selected ? new Date(selected+"-01T12:00:00") : new Date();
  const months = Array.from({length:6},(_,i)=>{
    const d = new Date(anchor.getFullYear(),anchor.getMonth()-5+i,1);
    const key = d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0");
    const category=$("#category-filter").value;
    return {label:d.toLocaleDateString("en-IN",{month:"short"}),key,amount:allExpenses.filter(x=>x.date.startsWith(key)&&(!category||x.category===category)).reduce((s,x)=>s+x.amount,0)};
  });
  const max = Math.max(1,...months.map(x=>x.amount));
  $("#monthly-chart").replaceChildren();
  $("#monthly-chart").setAttribute("aria-label",months.map(x=>x.key+": "+money(x.amount)).join(", "));
  months.forEach(x=>{
    const col=document.createElement("div");col.className="month-col";
    const value=document.createElement("span");value.className="value";value.textContent="₹"+compact(x.amount);
    const space=document.createElement("div");space.className="bar-space";
    const bar=document.createElement("div");bar.className="bar";bar.style.height=(x.amount/max*100)+"%";bar.title=x.key+": "+money(x.amount);
    space.append(bar);const label=document.createElement("small");label.textContent=x.label;
    col.append(value,space,label);$("#monthly-chart").append(col);
  });
}
function render() {
  const items=filteredExpenses(), sum=items.reduce((s,x)=>s+x.amount,0);
  $("#total").textContent=money(sum);$("#count").textContent=String(items.length);$("#average").textContent=money(items.length?sum/items.length:0);
  $("#results-label").textContent=items.length+" transaction"+(items.length===1?"":"s");
  drawCategoryChart(items);drawMonthlyChart();renderBudget();
  $("#expenses").replaceChildren();
  if(!items.length){const p=document.createElement("p");p.className="empty";p.textContent="No expenses match your filters.";$("#expenses").append(p);}
  items.forEach(item=>{
    const row=document.createElement("div");row.className="expense";
    const info=document.createElement("div"),name=document.createElement("strong"),detail=document.createElement("small");
    name.textContent=item.title;detail.textContent=item.category+" • "+item.date;info.append(name,detail);
    const right=document.createElement("div");right.className="right";
    const amount=document.createElement("strong");amount.textContent=money(item.amount);
    const edit=document.createElement("button");edit.className="edit";edit.textContent="Edit";edit.addEventListener("click",()=>startEdit(item));
    const button=document.createElement("button");button.className="delete";button.textContent="Delete";
    button.addEventListener("click",()=>removeExpense(item.id));right.append(amount,edit,button);row.append(info,right);$("#expenses").append(row);
  });
}
async function loadExpenses(){
  try{const response=await secureFetch("/api/expenses");if(!response.ok)throw Error("Could not load expenses.");
    allExpenses=await response.json();render();
  }catch(error){$("#message").textContent=error.message;}
}
async function removeExpense(id){
  try{const response=await secureFetch("/api/expenses/"+id,{method:"DELETE"});if(!response.ok)throw Error("Could not delete expense.");
    $("#message").textContent="";await loadExpenses();
  }catch(error){$("#message").textContent=error.message;}
}
$("#expense-form").addEventListener("submit",async event=>{
  event.preventDefault();$("#message").textContent="";
  const payload={title:$("#title").value.trim(),amount:Number($("#amount").value),category:$("#category").value,date:$("#date").value};
  try{const response=await secureFetch(editingId===null?"/api/expenses":"/api/expenses/"+editingId,{method:editingId===null?"POST":"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
    const result=await response.json();if(!response.ok)throw Error(result.error||"Could not add expense.");
    resetEdit();await loadExpenses();
  }catch(error){$("#message").textContent=error.message;}
});
$("#month-filter").addEventListener("change",()=>{loadBudget();render();});
$("#category-filter").addEventListener("change",render);
$("#clear-filters").addEventListener("click",()=>{$("#month-filter").value="";$("#category-filter").value="";loadBudget();render();});
$("#export-csv").addEventListener("click",()=>{
  const rows=[["Date","Title","Category","Amount (INR)"],...filteredExpenses().map(x=>[x.date,x.title,x.category,x.amount])];
  const csv=rows.map(row=>row.map(value=>'"'+String(value).replace(/"/g,'""')+'"').join(",")).join("\r\n");
  const blob=new Blob(["\uFEFF"+csv],{type:"text/csv;charset=utf-8"});
  const url=URL.createObjectURL(blob),link=document.createElement("a");
  link.href=url;link.download="expense-report-"+($("#month-filter").value||"all-time")+".csv";
  document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
});
loadExpenses();

function resetEdit(){
  editingId=null;$("#expense-form").reset();$("#date").value=localToday();
  $("#expense-form-heading").textContent="Add an expense";$("#submit-expense").textContent="Add expense";
  $("#cancel-edit").hidden=true;
}
function startEdit(item){
  editingId=item.id;$("#title").value=item.title;$("#amount").value=item.amount;
  $("#category").value=item.category;$("#date").value=item.date;
  $("#expense-form-heading").textContent="Edit expense";$("#submit-expense").textContent="Save changes";
  $("#cancel-edit").hidden=false;$("#expense-form").scrollIntoView({behavior:"smooth",block:"center"});
}
$("#cancel-edit").addEventListener("click",resetEdit);
function budgetMonth(){return $("#month-filter").value || localToday().slice(0,7);}
async function loadBudget(){
  const month=budgetMonth();
  $("#budget-month-label").textContent=month;
  try{
    const response=await secureFetch("/api/budgets/"+month);
    if(!response.ok)throw Error("Could not load budget.");
    const result=await response.json();
    if(month!==budgetMonth())return;
    activeBudget=result.amount;
    $("#budget-amount").value=activeBudget??"";
    renderBudget();
  }catch(error){$("#budget-warning").textContent=error.message;}
}
function renderBudget(){
  const month=budgetMonth();
  const spent=allExpenses.filter(x=>x.date.startsWith(month)).reduce((sum,x)=>sum+x.amount,0);
  const limit=activeBudget;
  const ratio=limit?spent/limit:0;
  $("#budget-status").textContent=limit?money(spent)+" of "+money(limit)+" used":"No budget set for "+month;
  $("#budget-remaining").textContent=limit?(spent>limit?money(spent-limit)+" over budget":money(limit-spent)+" remaining"):"";
  $("#budget-progress").style.width=Math.min(100,ratio*100)+"%";
  $("#budget-progress").classList.toggle("over",!!limit&&spent>limit);
  $("#budget-warning").textContent=limit&&spent>limit?"⚠ You have exceeded your monthly budget.":limit&&ratio>=0.8?"You have used at least 80% of your budget.":"";
}
$("#budget-form").addEventListener("submit",async event=>{
  event.preventDefault();
  const month=budgetMonth(),amount=Number($("#budget-amount").value);
  try{
    const response=await secureFetch("/api/budgets/"+month,{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify({amount})});
    const result=await response.json();if(!response.ok)throw Error(result.error||"Could not save budget.");
    activeBudget=result.amount;renderBudget();
  }catch(error){$("#budget-warning").textContent=error.message;}
});
loadBudget();
