(defun laba ()
    (setq x "0" y "0" plotM "32" plotN "32" result 1 color 255 i 0)
    (setq dcl_id (load_dialog "C:\\Users\\Admin\\Downloads\\Lisp\\dcl.dcl"))
    
    (while (>= result 1)
        (if (not (new_dialog "lab" dcl_id))
            (progn(alert "Ошибка при загрузке dcl файла!")
                (exit))
        )
        (set_tile "pl_m" plotM)
        (set_tile "pl_n" plotN)
        (set_tile "pt_x" x)
        (set_tile "pt_y" y)
        (action_tile "accept" "(done_dialog 1)")
        (action_tile "cancel" "(setq result 0)")
        (action_tile "color" "(done_dialog 3)")
        (action_tile "mouse" "(done_dialog 2)")
        (action_tile "file" "(done_dialog 4)")
        (action_tile "pl_m" "(setq plotM $value)")
        (action_tile "pl_n" "(setq plotN $value)")
        (action_tile "pt_x" "(setq x $value)")
        (action_tile "pt_y" "(setq y $value)")

        (setq result (start_dialog))
        (if (= result 1) (draw))
        (if (= result 2) (get_point))
        (if (= result 3) (setq color (acad_colordlg color)))
        (if (= result 4) (setq source_file (getfiled "File" "C:\\Users\\Admin\\Downloads\\Lisp\\" "txt" 8)))
    )
    (unload_dialog dcl_id)
)

(defun get_point()
    (setq point (getpoint "Укажите точку, куда поместить объект"))
    (setq x (rtos (car point) 2 3))
    (setq y (rtos (cadr point) 2 3))
    (setq point0 (list (atoi x)  (atoi y)))
)

(defun draw()
    (command "color" color)
    (if (not point0)
        (setq point0 (list (atoi x)  (atoi y)))
    )
    (setq osm (getvar "osmode"))
  	(setvar "osmode" 0)
    (command "surftab1" plotM)
	(command "surftab2" plotN)
    (setq x (atoi x))
    (setq y (atoi y))
	(if (not source_file)
        (progn(alert "Ошибка! Файл не выбран.")
            (exit))
    )
    (setq file (open (findfile source_file) "r"))

    (setq s (read-line file))   

    (while (/= s "end")
	    (setq i (+ i 1))
        (command "_pline" point0)
		(while (/= s ".")
		    (cond
		        (
                    (= s "a")
				    (command "_a")
                )								            
		        (
                    (= s "dir")
				    (command "_dir")
                    (setq x (+ x (atof (setq s (read-line file)))) y (+ y (atof (setq s (read-line file)))))
			        (setq point2 (list x y))
                    (command point2)
                )
		        (
                    (/= s "a")
                    (setq x (+ x (atof s)) y (+ y (atof (setq s (read-line file)))))
			        (setq point2 (list x y))
                    (command point2)
                    (setq point0 point2)
                )
	        )
	        (setq s (read-line file))
        )
	    (command "")

	    (cond
            (
                (= i 1)
	            (setq a (entlast))
            )
            (
                (= i 2)
	            (setq b (entlast))
            )
            (
                (= i 3)
	            (setq c (entlast))
            )
            (
                (= i 4)
	            (setq d (entlast))
            )
        )

        (setq s (read-line file))
    )

    (command "_edgesurf" a b c d)
  
  	(setvar "osmode" osm)
)

(laba)
