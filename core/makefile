# Each target builds one f2py module next to its source, under the name the
# Python code imports. f2py builds with meson on Python 3.12, which can't take a
# path in -m, hence the cd.
F2PY = f2py3 --quiet -c

MODULES = world2vox_fortran g_genhsphere g_genssphere gen_central_glow_f g_shooting_star_f \
          g_ellipsoid g_torus_f gen_outer_shadow_f

all: $(MODULES)

world2vox_fortran:
	@echo 'compiling world2vox...'
	@$(F2PY) -m world2vox_fortran world2vox_revis.f90

g_genhsphere:
	@echo 'compiling g_genhsphere...'
	@cd generators && $(F2PY) -m g_genhsphere g_growing_sphere.f90

g_genssphere:
	@echo 'compiling g_genssphere...'
	@cd generators && $(F2PY) -m g_genssphere g_growing_sphere_solid.f90

gen_central_glow_f:
	@echo 'compiling gen_central_glow_f...'
	@cd generators && $(F2PY) -m gen_central_glow_f g_central_glow_f.f90

g_shooting_star_f:
	@echo 'compiling g_shooting_star_f...'
	@cd generators && $(F2PY) -m g_shooting_star_f g_shooting_star_f.f90

g_ellipsoid:
	@echo 'compiling g_ellipsoid...'
	@cd generators && $(F2PY) -m g_ellipsoid g_ellipsoid_f.f90

g_torus_f:
	@echo 'compiling g_torus_f...'
	@cd generators && $(F2PY) -m g_torus_f g_torus.f90

gen_outer_shadow_f:
	@echo 'compiling gen_outer_shadow_f...'
	@cd effects && $(F2PY) -m gen_outer_shadow_f e_outer_shadow_f.f90

clean:
	@echo 'Cleaning up...'
	$(RM) *.so
	$(RM) *.pyc
	$(RM) generators/*.so
	$(RM) generators/*.pyc
	$(RM) effects/*.so
	$(RM) effects/*.pyc
