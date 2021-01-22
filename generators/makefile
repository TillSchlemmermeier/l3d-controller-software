all: say_hello world2vox_fortran

say_hello:
	@echo ''
	@echo 'starting make process...'
	@echo ''

world2vox_fortran:
	@echo 'compiling world2vox...'
	@f2py3 --quiet -c -m g_genhsphere g_growing_sphere.f90
	@f2py3 --quiet -c -m g_gentorus g_torus.f90
	@f2py3 --quiet -c -m gen_central_glow_f g_central_glow_f.f90
	@f2py3 --quiet -c -m g_ellipsoid g_ellipsoid_f.f90
	@f2py3 --quiet -c -m g_genssphere g_growing_sphere_solid.f90
	@f2py3 --quiet -c -m g_shooting_star_f g_shooting_star_f.f90
	@f2py3 --quiet -c -m g_sphere_f g_sphere_f.f90
	@f2py3 --quiet -c -m test g_torus.f90

clean:
	@echo 'Cleaning up...'
	$(RM) *.so
	$(RM) *.pyc
