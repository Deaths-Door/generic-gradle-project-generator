
from src.gradle.buildgradle import ModuleBuildGradle
from src.gradle.dependency import Dependency, DependencyGroup, DependencyType
from src.gradle.plugin import Plugin, PluginGroup, PluginWithCodeBlock, alias

def create_plugin_group() :
    plugin_with_code_block0 = PluginWithCodeBlock(Plugin.alias("libs.kotlin_multiplatform"))
    plugin_with_code_block0.code = """
    kotlin {
        androidTarget {
            compilations.all {
                kotlinOptions {
                    jvmTarget = "17"
                }
            }
        }
    }
    """

    plugin_with_code_block1 = PluginWithCodeBlock(Plugin.alias("libs.android"))
    plugin_with_code_block1.code = """
    android {
        namespace = "com.deathsdoor.chillback"
        compileSdk = libs.versions.android.compileSdk.get().toInt()

        sourceSets["main"].manifest.srcFile("src/androidMain/AndroidManifest.xml")
        sourceSets["main"].res.srcDirs("src/androidMain/res")
        sourceSets["main"].resources.srcDirs("src/commonMain/resources")

        defaultConfig {
            applicationId = "com.deathsdoor.chillback"
            minSdk = libs.versions.android.minSdk.get().toInt()
            targetSdk = libs.versions.android.targetSdk.get().toInt()
            versionCode = 1
            versionName = "1.0"
        }
    }
    """

    return PluginGroup([
        alias("libs.datastore"),
        alias("libs.astroplayer"),
        plugin_with_code_block0,
        plugin_with_code_block1
    ])


def create_dependency_group() :
    return DependencyGroup([
        Dependency(DependencyType.Implementation, "com.squareup.retrofit2:retrofit:2.9.0"),
        Dependency(DependencyType.Implementation, "com.squareup.okhttp3:okhttp:4.9.3"),
        Dependency.from_seperated(type=DependencyType.Api,group_id="com.google.code.gson",artifact_id= "gson",version= "2.9.0")
    ])

module_build_gradle = ModuleBuildGradle(
    plugins=create_plugin_group(),
    dependencies=create_dependency_group(),
    other=None,
)

print(str(module_build_gradle))