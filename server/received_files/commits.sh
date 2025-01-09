#!/bin/bash

# Hacer múltiples commits vacíos del 1 de septiembre al 30 de septiembre de 2024
for d in {01..30}
do
  for i in {1..15}  # Cambia este número para hacer más o menos commits por día
  do
    # Ajuste para que los minutos tengan dos dígitos correctamente
    if [ $i -lt 10 ]; then
      minute="0$i"
    else
      minute="$i"
    fi

    # Establecer la fecha para el autor y el committer
    export GIT_COMMITTER_DATE="2024-09-$d 12:$minute:00"
    GIT_AUTHOR_DATE="2024-09-$d 12:$minute:00" git commit --allow-empty -m "Commit del día 2024-09-$d, número $i" --date="2024-09-$d 12:$minute:00"
  done
done

# Push al repositorio remoto
git push origin main
