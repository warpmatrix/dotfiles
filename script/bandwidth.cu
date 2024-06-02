#include <cuda_runtime.h>
#include <iostream>
#include <chrono>

#define CHECK_CUDA_ERROR(call) \
	do { \
		cudaError_t error = call; \
		if (error != cudaSuccess) { \
			std::cerr << "CUDA Error: " << cudaGetErrorString(error) << " at " << __FILE__ << ":" << __LINE__ << std::endl; \
			exit(EXIT_FAILURE); \
		} \
	} while (0)

int main() {
	const size_t size = 1024 * 1024 * 1024; // 100 MB
	float *h_data = (float*)malloc(size);
	float *d_data;

	CHECK_CUDA_ERROR(cudaMalloc((void**)&d_data, size));

	cudaEvent_t start, stop;
	CHECK_CUDA_ERROR(cudaEventCreate(&start));
	CHECK_CUDA_ERROR(cudaEventCreate(&stop));

    std::cout << "begin transfer" << '\n';
	CHECK_CUDA_ERROR(cudaEventRecord(start, 0));
    int times = 100;
    for (int i = 0; i < times; i++) {
        CHECK_CUDA_ERROR(cudaMemcpy(d_data, h_data, size, cudaMemcpyHostToDevice));
    }
	CHECK_CUDA_ERROR(cudaEventRecord(stop, 0));

	CHECK_CUDA_ERROR(cudaEventSynchronize(stop));
    std::cout << "end transfer" << '\n';

	float milliseconds = 0;
	CHECK_CUDA_ERROR(cudaEventElapsedTime(&milliseconds, start, stop));

	float bandwidth = times * (size / (1 << 20)) / (milliseconds / 1000.0f);
	std::cout << "Host to Device Bandwidth: " << bandwidth << " MB/s" << std::endl;
    std::cout << "Transfer time: " << milliseconds / 1000.0f << " s" << std::endl;
    std::cout << "Transfer size: " << times * (size / (1 << 20)) << " MB" << std::endl;

	CHECK_CUDA_ERROR(cudaEventDestroy(start));
	CHECK_CUDA_ERROR(cudaEventDestroy(stop));
	CHECK_CUDA_ERROR(cudaFree(d_data));
	free(h_data);
	return 0;
}
