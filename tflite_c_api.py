import ctypes
import os


class TFLiteLibrary:
    """Singleton wrapper for loading the TFLite native library"""
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        lib_path = self._find_library()
        self._lib = ctypes.cdll.LoadLibrary(lib_path)
        self._setup_function_signatures()

    def _find_library(self):
        """Find the TFLite native library in common locations"""
        # 1. Check LD_LIBRARY_PATH first (Android native lib dir)
        ld_library_path = os.environ.get('LD_LIBRARY_PATH', '')
        for p in ld_library_path.split(':'):
            p = p.strip()
            if p:
                full_path = os.path.join(p, 'libtensorflowlite_jni.so')
                if os.path.exists(full_path):
                    return full_path

        # 2. Check app bundle dir
        bundle_dir = os.path.join(os.path.dirname(__file__), 'libs', 'android-v8', 'libtensorflowlite_jni.so')
        if os.path.exists(bundle_dir):
            return bundle_dir

        # 3. Check system paths
        possible_paths = [
            '/system/lib64/libtensorflowlite_jni.so',
            '/system/lib/libtensorflowlite_jni.so',
            '/data/app/libtensorflowlite_jni.so',
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path

        # 4. Fallback to system loader
        return 'libtensorflowlite_jni.so'

    def __getattr__(self, name):
        """Delegate attribute access to the underlying CDLL object"""
        if name.startswith('_'):
            raise AttributeError(name)
        return getattr(self._lib, name)

    def _setup_function_signatures(self):
        lib = self._lib

        # --- Model functions ---
        # TfLiteModel* TfLiteModelCreateFromFile(const char* model_path)
        lib.TfLiteModelCreateFromFile.argtypes = [ctypes.c_char_p]
        lib.TfLiteModelCreateFromFile.restype = ctypes.c_void_p

        # void TfLiteModelDelete(TfLiteModel* model)
        lib.TfLiteModelDelete.argtypes = [ctypes.c_void_p]
        lib.TfLiteModelDelete.restype = None

        # --- InterpreterOptions functions ---
        # TfLiteInterpreterOptions* TfLiteInterpreterOptionsCreate()
        lib.TfLiteInterpreterOptionsCreate.argtypes = []
        lib.TfLiteInterpreterOptionsCreate.restype = ctypes.c_void_p

        # void TfLiteInterpreterOptionsSetNumThreads(TfLiteInterpreterOptions* options, int num_threads)
        lib.TfLiteInterpreterOptionsSetNumThreads.argtypes = [ctypes.c_void_p, ctypes.c_int]
        lib.TfLiteInterpreterOptionsSetNumThreads.restype = None

        # void TfLiteInterpreterOptionsDelete(TfLiteInterpreterOptions* options)
        lib.TfLiteInterpreterOptionsDelete.argtypes = [ctypes.c_void_p]
        lib.TfLiteInterpreterOptionsDelete.restype = None

        # --- Interpreter functions ---
        # TfLiteInterpreter* TfLiteInterpreterCreate(TfLiteModel* model, TfLiteInterpreterOptions* options)
        lib.TfLiteInterpreterCreate.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        lib.TfLiteInterpreterCreate.restype = ctypes.c_void_p

        # void TfLiteInterpreterDelete(TfLiteInterpreter* interpreter)
        lib.TfLiteInterpreterDelete.argtypes = [ctypes.c_void_p]
        lib.TfLiteInterpreterDelete.restype = None

        # TfLiteStatus TfLiteInterpreterAllocateTensors(TfLiteInterpreter* interpreter)
        lib.TfLiteInterpreterAllocateTensors.argtypes = [ctypes.c_void_p]
        lib.TfLiteInterpreterAllocateTensors.restype = ctypes.c_int

        # TfLiteStatus TfLiteInterpreterInvoke(TfLiteInterpreter* interpreter)
        lib.TfLiteInterpreterInvoke.argtypes = [ctypes.c_void_p]
        lib.TfLiteInterpreterInvoke.restype = ctypes.c_int

        # TfLiteTensor* TfLiteInterpreterGetInputTensor(TfLiteInterpreter* interpreter, int index)
        lib.TfLiteInterpreterGetInputTensor.argtypes = [ctypes.c_void_p, ctypes.c_int]
        lib.TfLiteInterpreterGetInputTensor.restype = ctypes.c_void_p

        # TfLiteTensor* TfLiteInterpreterGetOutputTensor(TfLiteInterpreter* interpreter, int index)
        lib.TfLiteInterpreterGetOutputTensor.argtypes = [ctypes.c_void_p, ctypes.c_int]
        lib.TfLiteInterpreterGetOutputTensor.restype = ctypes.c_void_p

        # --- Tensor functions ---
        # TfLiteType TfLiteTensorType(const TfLiteTensor* tensor)
        lib.TfLiteTensorType.argtypes = [ctypes.c_void_p]
        lib.TfLiteTensorType.restype = ctypes.c_int

        # int TfLiteTensorNumDims(const TfLiteTensor* tensor)
        lib.TfLiteTensorNumDims.argtypes = [ctypes.c_void_p]
        lib.TfLiteTensorNumDims.restype = ctypes.c_int

        # int TfLiteTensorDim(const TfLiteTensor* tensor, int dim_index)
        lib.TfLiteTensorDim.argtypes = [ctypes.c_void_p, ctypes.c_int]
        lib.TfLiteTensorDim.restype = ctypes.c_int

        # size_t TfLiteTensorByteSize(const TfLiteTensor* tensor)
        lib.TfLiteTensorByteSize.argtypes = [ctypes.c_void_p]
        lib.TfLiteTensorByteSize.restype = ctypes.c_size_t

        # TfLiteStatus TfLiteTensorCopyFromBuffer(TfLiteTensor* tensor, const void* input_data, size_t input_data_size)
        lib.TfLiteTensorCopyFromBuffer.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]
        lib.TfLiteTensorCopyFromBuffer.restype = ctypes.c_int

        # TfLiteStatus TfLiteTensorCopyToBuffer(const TfLiteTensor* tensor, void* output_data, size_t output_data_size)
        lib.TfLiteTensorCopyToBuffer.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]
        lib.TfLiteTensorCopyToBuffer.restype = ctypes.c_int


class TFLiteInterpreter:
    """High-level Python wrapper for TFLite C API"""

    def __init__(self, model_path, num_threads=2):
        self._lib = TFLiteLibrary.get_instance()

        # Load model
        model_path_b = model_path.encode('utf-8') if isinstance(model_path, str) else model_path
        self._model = self._lib.TfLiteModelCreateFromFile(model_path_b)
        if not self._model:
            raise RuntimeError(f"Failed to create model from: {model_path}")

        # Create options
        self._options = self._lib.TfLiteInterpreterOptionsCreate()
        self._lib.TfLiteInterpreterOptionsSetNumThreads(self._options, num_threads)

        # Create interpreter
        self._interpreter = self._lib.TfLiteInterpreterCreate(self._model, self._options)
        if not self._interpreter:
            self._lib.TfLiteModelDelete(self._model)
            self._lib.TfLiteInterpreterOptionsDelete(self._options)
            raise RuntimeError("Failed to create interpreter")

        # Allocate tensors
        status = self._lib.TfLiteInterpreterAllocateTensors(self._interpreter)
        if status != 0:
            self._cleanup()
            raise RuntimeError(f"Failed to allocate tensors: status={status}")

        # Get input/output tensor info
        self._input_tensor = self._lib.TfLiteInterpreterGetInputTensor(self._interpreter, 0)
        self._output_tensor = self._lib.TfLiteInterpreterGetOutputTensor(self._interpreter, 0)

        self.input_size = self._lib.TfLiteTensorByteSize(self._input_tensor)
        self.output_size = self._lib.TfLiteTensorByteSize(self._output_tensor)

        input_dims = self._lib.TfLiteTensorNumDims(self._input_tensor)
        self.input_shape = tuple(
            self._lib.TfLiteTensorDim(self._input_tensor, i) for i in range(input_dims)
        )

        output_dims = self._lib.TfLiteTensorNumDims(self._output_tensor)
        self.output_shape = tuple(
            self._lib.TfLiteTensorDim(self._output_tensor, i) for i in range(output_dims)
        )

    def _cleanup(self):
        if hasattr(self, '_interpreter') and self._interpreter:
            self._lib.TfLiteInterpreterDelete(self._interpreter)
            self._interpreter = None
        if hasattr(self, '_options') and self._options:
            self._lib.TfLiteInterpreterOptionsDelete(self._options)
            self._options = None
        if hasattr(self, '_model') and self._model:
            self._lib.TfLiteModelDelete(self._model)
            self._model = None

    def __del__(self):
        if hasattr(self, '_lib'):
            self._cleanup()

    def get_input_tensor(self):
        """Get the input tensor pointer"""
        return self._lib.TfLiteInterpreterGetInputTensor(self._interpreter, 0)

    def get_output_tensor(self):
        """Get the output tensor pointer"""
        return self._lib.TfLiteInterpreterGetOutputTensor(self._interpreter, 0)

    def run(self, input_array, output_array):
        """
        Run inference with ctypes arrays.

        Args:
            input_array: ctypes array of floats (e.g., (ctypes.c_float * size)(*data))
            output_array: ctypes array of floats (e.g., (ctypes.c_float * output_size)())
        """
        # Copy input data to input tensor
        status = self._lib.TfLiteTensorCopyFromBuffer(
            self._input_tensor,
            ctypes.cast(input_array, ctypes.c_void_p),
            ctypes.sizeof(input_array)
        )
        if status != 0:
            raise RuntimeError(f"Failed to copy input data: status={status}")

        # Run inference
        status = self._lib.TfLiteInterpreterInvoke(self._interpreter)
        if status != 0:
            raise RuntimeError(f"Failed to invoke interpreter: status={status}")

        # Copy output data from output tensor
        status = self._lib.TfLiteTensorCopyToBuffer(
            self._output_tensor,
            ctypes.cast(output_array, ctypes.c_void_p),
            ctypes.sizeof(output_array)
        )
        if status != 0:
            raise RuntimeError(f"Failed to copy output data: status={status}")