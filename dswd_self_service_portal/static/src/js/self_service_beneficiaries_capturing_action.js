var family_members = [];
var family_member_index = 0;
var family_member_count = document.getElementById("family_member_count")
function add_new_row(btn) {
    var table = document.getElementById("tbl_family_members");
    
    if(validate_family_member()){
        btn.style="display:none"
        family_member_count.value=family_member_index+1
        create_new_row(table)
        
            
    }
}

function validate_family_member() {
    var isValid = true
    input_name = document.getElementById("family_member_"+family_member_index+"_name");
    if(!input_name.value){
        invalidate_field(input_name)
        isValid = false;
    } else {
        reset_invalidate_field(input_name)
    }

    input_relations = document.getElementById("family_member_"+family_member_index+"_relations");
    if(input_relations.selectedIndex<0){
        invalidate_field(input_relations);
        isValid = false;
    }else {
        reset_invalidate_field(input_relations)
    }

    input_dob = document.getElementById("family_member_"+family_member_index+"_dob");
    if(!input_dob.value){
        invalidate_field(input_dob);
        isValid = false;
    }else {
        reset_invalidate_field(input_dob)
    }

    input_occupation = document.getElementById("family_member_"+family_member_index+"_occupation");
    if(!input_occupation.value){
        invalidate_field(input_occupation)
        isValid = false;
    }else {
        reset_invalidate_field(input_occupation)
    }

    input_income = document.getElementById("family_member_"+family_member_index+"_income");
    if(!input_income.value){
        invalidate_field(input_income);
        isValid = false;
    }else {
        reset_invalidate_field(input_income)
    }
    return isValid;
}
function invalidate_field(field) {
    field.setAttribute("style","border:solid red 1px")
}
function reset_invalidate_field(field) {
    field.setAttribute("style","border:none")
}

function create_new_row(table,family_member) {
    var row = table.insertRow(-1);
    family_member_index++;
    console.log(family_member)
    var td_fullname = row.insertCell(0);
    td_fullname.id = "td_family_member_" + family_member_index + "_name"
    var input_name = document.createElement("input");
    input_name.type = "textbox";
    input_name.id = "family_member_" + family_member_index + "_name";
    input_name.name = "family_member_" + family_member_index + "_name";
    if(family_member){
     input_name.value=family_member.name
    }
    
    input_name.classList.add("form-control"); 
    td_fullname.appendChild(input_name)


    var td_relations = row.insertCell(1);
    td_relations.id = "td_family_member_" + family_member_index + "_relations";
    var select_relations = document.createElement("select");
    select_relations.id = "family_member_" + family_member_index + "_relations";
    select_relations.name = "family_member_" + family_member_index + "_relations";
    if(family_member){
      for (var i = 0; i < relationshipsData.length; i++) {
        var option = document.createElement("option");
        option.value = relationshipsData[i];
        option.text = relationshipsData[i];
        select_relations.appendChild(option);
        if(option.value===family_member.relation){
          select_relations.value=option.value
        }
    }
  
     }else{
      for (var i = 0; i < relationshipsData.length; i++) {
        var option = document.createElement("option");
        option.value = relationshipsData[i];
        option.text = relationshipsData[i];
        select_relations.appendChild(option);
    }
     }
  
  
    select_relations.classList.add("form-control")
    td_relations.appendChild(select_relations);
       
    var td_dob = row.insertCell(2);
    td_dob.id = "td_family_member_" + family_member_index + "_dob"
    var input_dob = document.createElement("input");
    input_dob.type = "date";
    input_dob.id = "family_member_" + family_member_index + "_dob";
    input_dob.name = "family_member_" + family_member_index + "_dob";
    if(family_member){
      input_dob.value=String(family_member.dob)
     }
    input_dob.classList.add("form-control");
    td_dob.appendChild(input_dob)

    var td_occupation = row.insertCell(3);
    td_occupation.id = "td_family_member_" + family_member_index + "_occupation"
    var input_occupation = document.createElement("input");
    input_occupation.type = "textbox";
    input_occupation.id = "family_member_" + family_member_index + "_occupation";
    input_occupation.name = "family_member_" + family_member_index + "_occupation";
    if(family_member){
      input_occupation.value=family_member.occupation
     }
    input_occupation.classList.add("form-control");
    td_occupation.appendChild(input_occupation);

    var td_monthly_income = row.insertCell(4);
    td_monthly_income.id = "td_family_member_" + family_member_index + "_income"
    var input_income = document.createElement("input");
    input_income.type = "textbox";
    input_income.id = "family_member_" + family_member_index + "_income";
    input_income.name = "family_member_" + family_member_index + "_income";
    if(family_member){
      input_income.value=family_member.income
     }
    input_income.classList.add("form-control");
    td_monthly_income.appendChild(input_income);

    var td_button = row.insertCell(5);
    console.log('if',family_member_count.value,family_member_index)
    if (family_member_index==family_member_count.value) {
      var input_button = document.createElement("button");
      input_button.type = "button"
      input_button.innerHTML = "Add"
      input_button.setAttribute("onclick", "add_new_row(this)");
      input_button.setAttribute("type", "button");
      td_button.appendChild(input_button);
    }
    
} 


let relationshipsData;

fetch('/get_relationships')
  .then(response => {
    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }
    return response.json();
  })
  .then(relations => {
    relationshipsData = relations;
    console.log('Relationships:', relations);
    // Handle the retrieved relationships data
    processRelationships(relationshipsData);
  })
  .catch(error => {
    console.error('Error getting relationships:', error);
  });

// Fetch family details data
fetch('/get_family_details')
  .then(response => {
    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }
    return response.json();
  })
  .then(familyDetails => {
    
    console.log('Family details:', familyDetails);
    // Handle the retrieved family details data
    processFamilyDetails(familyDetails);
  })
  .catch(error => {
    console.error('Error getting family details:', error);
  });

  // Function to process relationships data
function processRelationships(relations) {
  
  relations.forEach(relation => {
    // Access specific properties of each relation
    console.log('Relationship:', relation);
  });
  // Use the relationshipsData variable elsewhere in your code as needed
}

// Function to process family details data
function processFamilyDetails(familyDetails) {
  // Perform operations with the family details data here
  // Access individual elements, iterate over the array, etc.
  // Example:
  var familyTable=document.getElementById("tbl_family_members")
  if(familyDetails.length>0){
    family_member_count.value=familyDetails.length
    console.log("count",family_member_count.value)
    familyDetails.forEach(familyMember => {
      // Access specific properties of each family member

      create_new_row(familyTable,familyMember)
    });
  }

  
  // Use the familyDetailsData variable elsewhere in your code as needed
}





