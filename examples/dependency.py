
from src.gradle.dependency import *

if __name__ == "__main__":
    # Define a dependency of type "api" for the popular Gson library
    gson_dependency = Dependency(DependencyType.Api, "com.google.code.gson", "gson", "2.9.0")

    # Print the dependency string in Gradle format
    print(gson_dependency)  # Output: api("com.google.code.gson:gson:2.9.0")

    # -------------------------------- 

    # Define a dependency string with a specific version range
    kotlin_stdlib_dependency = "org.jetbrains.kotlin:kotlin-stdlib:1.7.0-beta"

    # Create a Dependency object from the string
    dependency = Dependency(DependencyType.Implementation, kotlin_stdlib_dependency)

    # Print the dependency string
    print(dependency)  # Output: implementation("org.jetbrains.kotlin:kotlin-stdlib:1.7.0-beta")

    # --------------------------------

    # Define a dependency of type "api" for the popular Gson library
    gson_dependency = Dependency(DependencyType.Api,"libs.datastore.android")

    # Print the dependency string in Gradle format
    print(gson_dependency)  # Output: api(libs.datastore.android)

    # --------------------------------
    # Define a test dependency using the Android-specific type
    test_runner_dependency = Dependency(AndroidDependencyType.TestImplementation, "androidx.test:runner:1.4.0")

    # Print the dependency string
    print(test_runner_dependency)  # Output: testImplementation("androidx.test:runner:1.4.0")

    # --------------------------------

    # Define dependencies
    retrofit_dependency = Dependency(DependencyType.Implementation, "com.squareup.retrofit2:retrofit:2.9.0")
    okhttp_dependency = Dependency(DependencyType.Implementation, "com.squareup.okhttp3:okhttp:4.9.3")

    # Group the dependencies
    dependency_group = DependencyGroup(retrofit_dependency)  # Pass the first dependency as initialization
    dependency_group.code.append(okhttp_dependency)

    # Print the formatted dependency block
    print(dependency_group)


    # --------------------------------

    # Define dependencies
    retrofit_dependency = Dependency(DependencyType.Implementation, "com.squareup.retrofit2:retrofit:2.9.0")
    okhttp_dependency = Dependency(DependencyType.Implementation, "com.squareup.okhttp3:okhttp:4.9.3")

    # Group the dependencies
    dependency_group = DependencyGroup([retrofit_dependency,okhttp_dependency]) 
    
    # Print the formatted dependency block
    print(dependency_group)



