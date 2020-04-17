not-empty = $(if $(strip $1),T)
empty = $(if $(strip $1),,T)

PIP := $(VIRTUAL_ENV)/bin/pip
which = which $1 || which $(VIRTUAL_ENV)/bin/$1 >/dev/null
RED=\e[0;31m
LRED=\e[1;31m
LCYAN=\e[96m
LYEL=\e[93m
NC=\e[0m

ARGS = $(filter-out $(word 1,$(MAKECMDGOALS)), $(MAKECMDGOALS))
FIRSTARG = $(if $(call empty, $(ARGS)),$(DEFAULTARG),$(word 1,$(ARGS)))

define err
echo -e "$(LRED)$(1)$(NC)"
endef

define warn
echo -e "$(LYEL)$(1)$(NC)"
endef

define inf
echo -e "$(LCYAN)$(1)$(NC)"
endef

# check-package(package)
#   Chequea si el paquete se encuentra instalado en el venv
define check-package
$(PIP) show --quiet $1
endef

# check-wd
#   Chequea primero si el working directory del repositorio git está limpio y
#   luego chequea si el staging area tambien se encuentra limpia.
#   Si, alguna de las condiciones falla, mensaje de error y devuelve 1
define check-wd
echo -n "Checking working directory..."
if git diff --quiet --exit-code ; then                 \
  $(call inf,ok)                                     ; \
else                                                   \
  $(call err,working directory not clean. Aborting)  ; \
  echo "Changes:"                                    ; \
  git diff --name-only                               ; \
  exit 1                                             ; \
fi
echo -n "Checking staging area..."
if git diff --cached --quiet --exit-code ; then        \
  $(call inf,ok)                                     ; \
else                                                   \
  $(call err,staging area not clean. Aborting)       ; \
  echo "Changes:"                                    ; \
  git diff --cached --name-only                      ; \
  exit 1                                             ; \
fi
endef

# assert-command-present(command)
# Chequea si existe un comando en el PATH o en el python environment definido
#	en VIRTUAL_ENV. Si no existe, entrega un mensaje de error y retorna 1
define assert-command-present
echo -n "Checking for $1..."
if $(call which,$1) ; then                              \
  $(call inf,ok)                                      ; \
else                                                    \
  $(call err,'$1' missing and needed for this build)  ; \
  exit 1                                              ; \
fi
endef

# check-create-branch(branch)
#   Chequea la existencia de un branch en el repo local
#   Si existe, nada. Si no existe, crea el branch
define check-create-branch
echo -n "Checking if $1 exists..."
if git rev-parse --verify --quiet $1 >/dev/null; then                     \
  $(call inf,ok)                                              ; \
else                                                            \
  $(call inf,branch $1 does not exist. Creating branch $1...) ; \
	git branch $1                                               ; \
fi
endef

# check-upstream(branch)
#   Chequea si hay cambios en el branch remoto. Para eso, actualiza los remote
#   tracking branches y compara con HEAD local. Si el remoto se encuentra
#   adelante, se escribe un mensaje y devuelve 1
define check-upstream
echo -n "Checking if there are any incoming changes on $1..."
git fetch --quiet >/dev/null
log=$$(git log $1..origin/$1 --oneline | wc -w)                      ; \
if [ $$log -eq 0 ]; then                                               \
  $(call inf,ok)                                                    ; \
else                                                                  \
  $(call warn,the branch $1 is behind origin/$1. You need to merge) ; \
  exit 1                                                            ; \
fi
endef
