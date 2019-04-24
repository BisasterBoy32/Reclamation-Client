
console.log("hello");

$("#info-personne").hide();
$("#info-entreprise").hide();

$("#personne").click(function(){
  $("#info-personne").show();
  $("#info-entreprise").hide();
  $("#f_name").attr("required" ,true);
  $("#l_name").attr("required" ,true);
  $("#e_name").attr("required" , false);
})

$("#enterprise").click(function(){
  $("#info-entreprise").show();
  $("#info-personne").hide();
  $("#f_name").attr("required" ,false);
  $("#l_name").attr("required" ,false);
  $("#e_name").attr("required" , true);
})
