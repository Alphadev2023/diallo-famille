document.addEventListener("DOMContentLoaded", function () {
  const genderField = document.querySelector("#id_genre");
  const militaryRow = document.querySelector(".form-row.field-mari");
  const date_naissance = document.querySelector("#id_date_naissance");
  const date_decce = document.querySelector(".form-row.field-date_decce");
  console.log(date_naissance.value.substr(0, 4));
  function toggleMilitaryRank() {
    if (!genderField || !militaryRow) return;

    if (genderField.value === "F") {
      militaryRow.style.display = "";
    } else {
      militaryRow.style.display = "none";
    }
  }

  toggleMilitaryRank(); // Initial load
  genderField.addEventListener("change", toggleMilitaryRank);
});
