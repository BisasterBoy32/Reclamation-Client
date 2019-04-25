
console.log("hello");

$(".info-personne").hide();
$(".info-entreprise").hide();

$("#personne").click(function(){
  $(".info-personne").show();
  $(".info-entreprise").hide();
  $("#f_name").attr("required" ,true);
  $("#l_name").attr("required" ,true);
  $("#p_region").attr("required" ,true);
  $("#p_rue").attr("required" ,true);
  $("#p_commune").attr("required" ,true);
  $("#p_logement").attr("required" ,true);

  $("#e_name").attr("required" , false);
  $("#e_region").attr("required" ,false);
  $("#e_rue").attr("required" ,false);
  $("#e_commune").attr("required" ,false);
})

$("#enterprise").click(function(){
  $(".info-entreprise").show();
  $(".info-personne").hide();
  $("#f_name").attr("required" ,false);
  $("#l_name").attr("required" ,false);
  $("#p_logement").attr("required" ,false);
  $("#p_region").attr("required" ,false);
  $("#p_rue").attr("required" ,false);
  $("#p_commune").attr("required" ,false);

  $("#e_name").attr("required" , true);
  $("#e_region").attr("required" ,true);
  $("#e_rue").attr("required" ,true);
  $("#e_commune").attr("required" ,true);
})
