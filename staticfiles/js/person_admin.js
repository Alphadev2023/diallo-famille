document.addEventListener("DOMContentLoaded", function () {
  const genderField = document.querySelector("#id_genre");
  const militaryRow = document.querySelector(".form-row.field-mari");
  const date_naissance = document.querySelector("#id_date_naissance");
  const est_vivant = document.querySelector("#id_est_vivant");
  const email = document.querySelector(".form-row.field-email");
  const tel = document.querySelector(".form-row.field-telephone");
  const dece = document.querySelector(".form-row.field-date_decce");
  const distric = document.querySelector(".form-row.field-district");
  const residence = document.querySelector(".form-row.field-reseidence_actuel");
  
  let date = new Date();
  let age_now = date_naissance.value.substr(0, 4);
  let age = parseInt(date.getFullYear()) - parseInt(age_now);
  console.log(age);
  function toggleMilitaryRank() {
    if (!genderField || !militaryRow || !est_vivant) return;

    if (genderField.value === "F") {
      militaryRow.style.display = "";
    }
    else {
      militaryRow.style.display = "none";
    }
  }

  function toggleEmail(){
     
    if(est_vivant.value === "D"){
      dece.style.display = "";
      tel.style.display = "none";
      email.style.display = "none";
      distric.style.display = "none";
      residence.style.display = "none";
    }else {
      dece.style.display = "none";
      email.style.display = "";
      tel.style.display = "";
      distric.style.display = "";
      residence.style.display = "";
    }
  }
 function toggleAge(){
    if(age < 12){
      email.style.display = "none";
      tel.style.display = "none";
      militaryRow.style.display = "none";
    }else{
    militaryRow.style.display = "";
    email.style.display = "";
    tel.style.display = "";
    }
  }

  toggleAge();
  toggleEmail();
  toggleMilitaryRank(); // Initial load
  genderField.addEventListener("change", toggleMilitaryRank);
  est_vivant.addEventListener("change", toggleEmail);
});
