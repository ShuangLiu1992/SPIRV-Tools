from conan import ConanFile
import conan.tools.files
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
import os


class SPIRVTOOLSConan(ConanFile):
    name = "spirv_tools"
    settings = "os", "compiler", "build_type", "arch"

    generators = "CMakeDeps"

    def generate(self):
        tc = CMakeToolchain(self)
        tc.presets_prefix = f"{self.settings.os}_{self.settings.build_type}_{self.settings.arch}"
        tc.variables["SPIRV_WERROR"] = False
        tc.variables["SPIRV_SKIP_EXECUTABLES"] = True
        tc.variables["SPIRV_SKIP_TESTS"] = True
        tc.variables['SPIRV-Headers_SOURCE_DIR'] = os.path.join(self.recipe_folder, "..", "SPIRV-Headers")
        tc.generate()

    def layout(self):
        cmake_layout(self)

    def package(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "none")
        self.cpp_info.set_property("cmake_file_name", "SPIRV-Tools")
        self.cpp_info.set_property("cmake_target_name", "SPIRV-Tools-static")
        if self.settings.os == "Windows":
            self.cpp_info.builddirs.append("SPIRV-Tools")
            self.cpp_info.builddirs.append("SPIRV-Tools-opt")
        else:
            self.cpp_info.builddirs.append(os.path.join("lib", "cmake"))
