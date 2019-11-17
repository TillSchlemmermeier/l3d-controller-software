all: say_hello world2vox_fortran

say_hello:
	@echo ''
	@echo 'starting make process...'
	@echo ''

world2vox_fortran: world2vox.f90
	@echo 'compiling world2vox...'
	@f2py3 --quiet -c -m world2vox_fortran world2vox.f90
	@f2py3 --quiet -c -m world2vox_fortran world2vox.f90
	cd generators;\
	f2py3 --quiet -c -m gen_central_glow_f g_central_glow_f.f90;\
	f2py3 -c -m g_genhsphere g_growing_sphere_f.f90;\
	f2py3 -c -m g_orbiter_big_f g_orbiter_big_f.f90;\
	f2py3 -c -m g_shooting_star_f g_shooting_star_f.f90;\
        f2py3 -c -m circle2d 2d_cirlce.f90;\
        f2py3 -c -m g_supernova_f g_supernova_f.f90;\
        f2py3 -c -m g_sphere_f g_sphere_f.f90;\
        f2py3 -c -m gen_gauss g_gauss_f.f90;\
        f2py3 -c -m circle2d 2d_circle.f90

clean:
	@echo 'Cleaning up...'
	$(RM) *.so
	$(RM) *.pyc
	$(RM) generators/*.so
	$(RM) generators/*.pyc
	$(RM) effects/*.so
	$(RM) effects/*.pyc
