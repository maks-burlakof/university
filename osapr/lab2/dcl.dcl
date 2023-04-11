lab: dialog {label = "Edge Surface";

	: spacer{height=1;}
	
	: boxed_column {label ="Точка вставки"; fixed_height = true;
	: edit_box {label = "Координата Х:"; key = "pt_x"; edit_width=10;}
 	: edit_box {label = "Координата Y:"; key = "pt_y"; edit_width=10;}
 	: spacer{height=1;}
 	: button { key = "mouse"; fixed_height = true; fixed_width = true; alignment = left; label = "Указать мышью -->  "; }
	
	}
	
	: spacer{height=0.1;}
	
	: boxed_row { label ="Плотность сетки:"; fixed_height = true;
	
 	: edit_box {label = "M-плотность:"; key = "pl_m"; edit_width=10;}
 	: edit_box {label = "N-плотность:"; key = "pl_n"; edit_width=10;}
 	
	}
	
	: row {
		: button { key = "file"; fixed_height = true; fixed_width = true; alignment = left; label = "Файл"; }
		: button { key = "color"; fixed_height = true; fixed_width = true; alignment = right; label = "Цвет"; }
	      }
	
	
	: spacer{height=0.2;}
ok_cancel; 

}