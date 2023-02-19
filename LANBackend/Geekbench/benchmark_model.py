from enum import Enum
from dataclasses import dataclass


class Result(Enum):
    SUCCESS = 0
    INVALID_URL = -1
    CONNECTION_ERROR = -2
    BENCHMARK_NOT_FOUND = -3


class TestKind(Enum):
    CPU = 0
    GPU = 1
    UNKNOWN = -1


@dataclass
class Benchmark:
    device: str
    test: TestKind
    system_information: dict
    cpu_information: dict
    memory_information: dict
    opencl_information: dict
    vulkan_information: dict
    single_core_performance: dict
    multi_core_performance: dict
    gpu_performance: dict

    def __init__(self):
        self.device = ""
        self.test = TestKind.UNKNOWN
        self.system_information = {}
        self.cpu_information = {}
        self.memory_information = {}
        self.opencl_information = {}
        self.vulkan_information = {}
        self.single_core_performance = {}
        self.multi_core_performance = {}
        self.gpu_performance = {}
        pass
