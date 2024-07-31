# flake8: noqa E501
from . import utils
import functools
import lazyllm

add_chinese_doc = functools.partial(utils.add_chinese_doc, module=lazyllm.components)
add_english_doc = functools.partial(utils.add_english_doc, module=lazyllm.components)
add_example = functools.partial(utils.add_example, module=lazyllm.components)

# Prompter
add_chinese_doc('Prompter', '''\
这是Prompter的文档
''')
add_english_doc('Prompter', '''\
This is doc for Prompter
''')
add_example('Prompter', '''\
def test_prompter():
    pass
''')

add_english_doc('Prompter.is_empty', '''\
This is doc for Prompter.is_empty
''')

add_chinese_doc('register', '''\
LazyLLM提供的Component的注册机制，可以将任意函数注册成LazyLLM的Component。被注册的函数无需显式的import，即可通过注册器提供的分组机制，在任一位置被索引到。

.. function:: register(cls, *, rewrite_func) -> Decorator

函数调用后返回一个装饰器，它会将被装饰的函数包装成一个Component注册到名为cls的组中.

Args:
    cls (str): 函数即将被注册到的组的名字，要求组必须存在，默认的组有 ``finetune`` 、 ``deploy`` ，用户可以调用 ``new_group`` 创建新的组
    rewrite_func (str): 注册后要重写的函数名称，默认为 ``apply`` ，当需要注册一个bash命令时需传入 ``cmd`` 

.. function:: register.cmd(cls) -> Decorator

函数调用后返回一个装饰器，它会将被装饰的函数包装成一个Component注册到名为cls的组中。被包装的函数需要返回一个可执行的bash命令。

Args:
    cls (str): 函数即将被注册到的组的名字，要求组必须存在，默认的组有 ``finetune`` 、 ``deploy`` ，用户可以调用 ``new_group`` 创建新的组

.. function:: register.new_group(group_name) -> None

新建一个ComponentGroup, 新建后的group会自动加入到__builtin__中，无需import即可在任一位置访问到该group.

Args:
    group_name (str): 待创建的group的名字
''')

add_english_doc('register', '''\
LazyLLM provides a registration mechanism for Components, allowing any function to be registered as a Component of LazyLLM. The registered functions can be indexed at any location through the grouping mechanism provided by the registrar, without the need for explicit import.

.. function:: register(cls, *, rewrite_func) -> Decorator

This function call returns a decorator that wraps the decorated function into a Component and registers it into the group named `cls`.

Args:
    cls (str): The name of the group to which the function will be registered. The group must exist. The default groups are `finetune` and `deploy`. Users can create new groups by calling `new_group`.
    rewrite_func (str): The name of the function to be rewritten after registration. The default is `'apply'`. If registering a bash command, pass `'cmd'`.

.. function:: register.cmd(cls) -> Decorator

This function call returns a decorator that wraps the decorated function into a Component and registers it into the group named `cls`. The wrapped function needs to return an executable bash command.

Args:
    cls (str): The name of the group to which the function will be registered. The group must exist. The default groups are `finetune` and `deploy`. Users can create new groups by calling `new_group`.

.. function:: register.new_group(group_name) -> None

Creates a new ComponentGroup. The newly created group will be automatically added to __builtin__ and can be accessed at any location without the need for import.

Args:
    group_name (str): The name of the group to be created.
''')

add_example('register', ['''\
>>> import lazyllm
>>> @lazyllm.component_register('mygroup')
... def myfunc(input):
...     return input
...
>>> lazyllm.mygroup.myfunc()(1)
1
''', '''\
>>> import lazyllm
>>> @lazyllm.component_register.cmd('mygroup')
... def mycmdfunc(input):
...     return f'echo {input}'
...
>>> lazyllm.mygroup.mycmdfunc()(1)
PID: 2024-06-01 00:00:00 lazyllm INFO: (lazyllm.launcher) Command: echo 1
PID: 2024-06-01 00:00:00 lazyllm INFO: (lazyllm.launcher) PID: 1
''', '''\
>>> import lazyllm
>>> lazyllm.component_register.new_group('mygroup')
>>> lazyllm.mygroup
{}
'''])

# ============= Finetune
# Finetune-AlpacaloraFinetune
add_chinese_doc('finetune.AlpacaloraFinetune', '''\
此类是 ``LazyLLMFinetuneBase`` 的子类，基于 [alpaca-lora](https://github.com/tloen/alpaca-lora) 项目提供的LoRA微调能力，用于对大语言模型进行LoRA微调。

Args:
    base_model (str): 用于进行微调的基模型的本地绝对路径。
    target_path (str): 微调后模型保存LoRA权重的本地绝对路径。
    merge_path (str): 模型合并LoRA权重后的路径，默认为 ``None`` 。如果未指定，则会在 ``target_path`` 下创建 "lora" 和 "merge" 目录，分别作为 ``target_path`` 和  ``merge_path`` 。
    model_name (str): 模型的名称，用于设置日志名的前缀，默认为 ``LLM``。
    cp_files (str): 指定复制源自基模型路径下的配置文件，会被复制到  ``merge_path`` ，默认为 ``tokeniz*``
    launcher (lazyllm.launcher): 微调的启动器，默认为 ``launchers.remote(ngpus=1)``。
    kw: 关键字参数，用于更新默认的训练参数。请注意，除了以下列出的关键字参数外，这里不能传入额外的关键字参数。

''')

add_english_doc('finetune.AlpacaloraFinetune', '''\
This class is a subclass of ``LazyLLMFinetuneBase``, based on the LoRA fine-tuning capabilities provided by the [alpaca-lora](https://github.com/tloen/alpaca-lora) project, used for LoRA fine-tuning of large language models.

Args:
    base_model (str): The base model used for fine-tuning. It is required to be the path of the base model.
    target_path (str): The path where the LoRA weights of the fine-tuned model are saved.
    merge_path (str): The path where the model merges the LoRA weights, default to `None`. If not specified, "lora" and "merge" directories will be created under ``target_path`` as ``target_path`` and ``merge_path`` respectively.
    model_name (str): The name of the model, used as the prefix for setting the log name, default to "LLM".
    cp_files (str): Specify configuration files to be copied from the base model path, which will be copied to ``merge_path``, default to ``tokeniz*``
    launcher (lazyllm.launcher): The launcher for fine-tuning, default to ``launchers.remote(ngpus=1)``.
    kw: Keyword arguments, used to update the default training parameters. Note that additional keyword arguments cannot be arbitrarily specified.

''')

add_example('finetune.AlpacaloraFinetune', '''\
>>> from lazyllm import finetune
>>> trainer = finetune.alpacalora('path/to/base/model', 'path/to/target')
''')

# Finetune-CollieFinetune
add_chinese_doc('finetune.CollieFinetune', '''\
此类是 ``LazyLLMFinetuneBase`` 的子类，基于 [Collie](https://github.com/OpenLMLab/collie) 框架提供的LoRA微调能力，用于对大语言模型进行LoRA微调。

Args:
    base_model (str): 用于进行微调的基模型。要求是基模型的路径。
    target_path (str): 微调后模型保存LoRA权重的路径。
    merge_path (str): 模型合并LoRA权重后的路径，默认为None。如果未指定，则会在 ``target_path`` 下创建 "lora" 和 "merge" 目录，分别作为 ``target_path`` 和  ``merge_path`` 。
    model_name (str): 模型的名称，用于设置日志名的前缀，默认为 "LLM"。
    cp_files (str): 指定复制源自基模型路径下的配置文件，会被复制到  ``merge_path`` ，默认为 "tokeniz\*"
    launcher (lazyllm.launcher): 微调的启动器，默认为 ``launchers.remote(ngpus=1)``。
    kw: 关键字参数，用于更新默认的训练参数。请注意，除了以下列出的关键字参数外，这里不能传入额外的关键字参数。

''')

add_english_doc('finetune.CollieFinetune', '''\
This class is a subclass of ``LazyLLMFinetuneBase``, based on the LoRA fine-tuning capabilities provided by the [Collie](https://github.com/OpenLMLab/collie) framework, used for LoRA fine-tuning of large language models.

Args:
    base_model (str): The base model used for fine-tuning. It is required to be the path of the base model.
    target_path (str): The path where the LoRA weights of the fine-tuned model are saved.
    merge_path (str): The path where the model merges the LoRA weights, default to ``None``. If not specified, "lora" and "merge" directories will be created under ``target_path`` as ``target_path`` and ``merge_path`` respectively.
    model_name (str): The name of the model, used as the prefix for setting the log name, default to "LLM".
    cp_files (str): Specify configuration files to be copied from the base model path, which will be copied to ``merge_path``, default to "tokeniz*"
    launcher (lazyllm.launcher): The launcher for fine-tuning, default to ``launchers.remote(ngpus=1)``.
    kw: Keyword arguments, used to update the default training parameters. Note that additional keyword arguments cannot be arbitrarily specified.

''')

add_example('finetune.CollieFinetune', '''\
>>> from lazyllm import finetune
>>> trainer = finetune.collie('path/to/base/model', 'path/to/target')
''')

# Finetune-LlamafactoryFinetune
add_chinese_doc('finetune.LlamafactoryFinetune', '''\
此类是 ``LazyLLMFinetuneBase`` 的子类，基于 [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) 框架提供的训练能力，用于对大语言模型(或视觉语言模型)进行训练。

Args:
    base_model (str): 用于进行训练的基模型。要求是基模型的路径。
    target_path (str): 训练后模型保存权重的路径。
    merge_path (str): 模型合并LoRA权重后的路径，默认为None。如果未指定，则会在 ``target_path`` 下创建 "lora" 和 "merge" 目录，分别作为 ``target_path`` 和  ``merge_path`` 。
    config_path (str): LLaMA-Factory的训练配置文件（这里要求格式为yaml），默认为None。如果未指定，则会在当前工作路径下，创建一个名为 ``.temp`` 的文件夹，并在其中生成以 ``train_`` 前缀开头，以 ``.yaml`` 结尾的配置文件。
    export_config_path (str): LLaMA-Factory的Lora权重合并的配置文件（这里要求格式为yaml），默认为None。如果未指定，则会在当前工作路径下中的 ``.temp`` 文件夹内生成以 ``merge_`` 前缀开头，以 ``.yaml`` 结尾的配置文件。
    launcher (lazyllm.launcher): 微调的启动器，默认为 ``launchers.remote(ngpus=1, sync=True)``。
    kw: 关键字参数，用于更新默认的训练参数。

''')

add_english_doc('finetune.LlamafactoryFinetune', '''\
This class is a subclass of ``LazyLLMFinetuneBase``, based on the training capabilities provided by the [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) framework, used for training large language models(or visual language models).

Args:
    base_model (str): The base model used for training. It is required to be the path of the base model.
    target_path (str): The path where the trained model weights are saved.
    merge_path (str): The path where the model is merged with LoRA weights, default is None. If not specified, "lora" and "merge" directories will be created under ``target_path``, to be used as ``target_path`` and ``merge_path`` respectively.
    config_path (str): The LLaMA-Factory training configuration file (yaml format is required), default is None. If not specified, a ``.temp`` folder will be created in the current working directory, and a configuration file starting with ``train_`` and ending with ``.yaml`` will be generated inside it.
    export_config_path (str): The LLaMA-Factory Lora weight merging configuration file (yaml format is required), default is None. If not specified, a configuration file starting with ``merge_`` and ending with ``.yaml`` will be generated inside the ``.temp`` folder in the current working directory.
    launcher (lazyllm.launcher): The launcher for fine-tuning, default is ``launchers.remote(ngpus=1, sync=True)``.
    kw: Keyword arguments used to update the default training parameters.

''')

add_example('finetune.LlamafactoryFinetune', '''\
>>> from lazyllm import finetune
>>> trainer = finetune.llamafactory('internlm2-chat-7b', 'path/to/target')
''')

# Finetune-Auto
add_chinese_doc('auto.AutoFinetune', '''\
此类是 ``LazyLLMFinetuneBase`` 的子类，可根据输入的参数自动选择合适的微调框架和参数，以对大语言模型进行微调。

具体而言，基于输入的：``base_model`` 的模型参数、``ctx_len``、``batch_size``、``lora_r``、``launcher`` 中GPU的类型以及卡数，该类可以自动选择出合适的微调框架（如: ``AlpacaloraFinetune`` 或 ``CollieFinetune``）及所需的参数。

Args:
    base_model (str): 用于进行微调的基模型。要求是基模型的路径。
    source (lazyllm.config['model_source']): 指定模型的下载源。可通过设置环境变量 ``LAZYLLM_MODEL_SOURCE`` 来配置，目前仅支持 ``huggingface`` 或 ``modelscope`` 。若不设置，lazyllm不会启动自动模型下载。
    target_path (str): 微调后模型保存LoRA权重的路径。
    merge_path (str): 模型合并LoRA权重后的路径，默认为 ``None``。如果未指定，则会在 ``target_path`` 下创建 "lora" 和 "merge" 目录，分别作为 ``target_path`` 和  ``merge_path`` 。
    ctx_len (int): 输入微调模型的token最大长度，默认为 ``1024``。
    batch_size (int): 批处理大小，默认为 ``32``。
    lora_r (int): LoRA 的秩，默认为 ``8``；该数值决定添加参数的量，数值越小参数量越小。
    launcher (lazyllm.launcher): 微调的启动器，默认为 ``launchers.remote(ngpus=1)``。
    kw: 关键字参数，用于更新默认的训练参数。注意这里能够指定的关键字参数取决于 LazyLLM 推测出的框架，因此建议谨慎设置。

''')

add_english_doc('auto.AutoFinetune', '''\
This class is a subclass of ``LazyLLMFinetuneBase`` and can automatically select the appropriate fine-tuning framework and parameters based on the input arguments to fine-tune large language models.

Specifically, based on the input model parameters of ``base_model``, ``ctx_len``, ``batch_size``, ``lora_r``, the type and number of GPUs in ``launcher``, this class can automatically select the appropriate fine-tuning framework (such as: ``AlpacaloraFinetune`` or ``CollieFinetune``) and the required parameters.

Args:
    base_model (str): The base model used for fine-tuning. It is required to be the path of the base model.
    source (lazyllm.config['model_source']): Specifies the model download source. This can be configured by setting the environment variable ``LAZYLLM_MODEL_SOURCE``.
    target_path (str): The path where the LoRA weights of the fine-tuned model are saved.
    merge_path (str): The path where the model merges the LoRA weights, default to ``None``. If not specified, "lora" and "merge" directories will be created under ``target_path`` as ``target_path`` and ``merge_path`` respectively.
    ctx_len (int): The maximum token length for input to the fine-tuned model, default to ``1024``.
    batch_size (int): Batch size, default to ``32``.
    lora_r (int): LoRA rank, default to ``8``; this value determines the amount of parameters added, the smaller the value, the fewer the parameters.
    launcher (lazyllm.launcher): The launcher for fine-tuning, default to ``launchers.remote(ngpus=1)``.
    kw: Keyword arguments, used to update the default training parameters. Note that additional keyword arguments cannot be arbitrarily specified, as they depend on the framework inferred by LazyLLM, so it is recommended to set them with caution.

''')

add_example('auto.AutoFinetune', '''\
>>> from lazyllm import finetune
>>> finetune.auto("Llama-7b", 'path/to/target')
<lazyllm.llm.finetune type=CollieFinetune>
''')

# ============= Deploy
# Deploy-Lightllm
add_chinese_doc('deploy.Lightllm', '''\
此类是 ``LazyLLMDeployBase`` 的子类，基于 [LightLLM](https://github.com/ModelTC/lightllm) 框架提供的推理能力，用于对大语言模型进行推理。

Args:
    trust_remote_code (bool): 是否允许加载来自远程服务器的模型代码，默认为 ``True``。
    launcher (lazyllm.launcher): 微调的启动器，默认为 ``launchers.remote(ngpus=1)``。
    stream (bool): 是否为流式响应，默认为 ``False``。
    kw: 关键字参数，用于更新默认的训练参数。请注意，除了以下列出的关键字参数外，这里不能传入额外的关键字参数。

''')

add_english_doc('deploy.Lightllm', '''\
This class is a subclass of ``LazyLLMDeployBase``, based on the inference capabilities provided by the [LightLLM](https://github.com/ModelTC/lightllm) framework, used for inference with large language models.

Args:
    trust_remote_code (bool): Whether to allow loading of model code from remote servers, default is ``True``.
    launcher (lazyllm.launcher): The launcher for fine-tuning, default is ``launchers.remote(ngpus=1)``.
    stream (bool): Whether the response is streaming, default is ``False``.
    kw: Keyword arguments used to update default training parameters. Note that not any additional keyword arguments can be specified here.

''')

add_example('deploy.Lightllm', '''\
>>> from lazyllm import deploy
>>> infer = deploy.lightllm()
''')

# Deploy-Vllm
add_chinese_doc('deploy.Vllm', '''\
此类是 ``LazyLLMDeployBase`` 的子类，基于 [VLLM](https://github.com/vllm-project/vllm) 框架提供的推理能力，用于对大语言模型进行推理。

Args:
    trust_remote_code (bool): 是否允许加载来自远程服务器的模型代码，默认为 ``True``。
    launcher (lazyllm.launcher): 微调的启动器，默认为 ``launchers.remote(ngpus=1)``。
    stream (bool): 是否为流式响应，默认为 ``False``。
    kw: 关键字参数，用于更新默认的训练参数。请注意，除了以下列出的关键字参数外，这里不能传入额外的关键字参数。

''')

add_english_doc('deploy.Vllm', '''\
This class is a subclass of ``LazyLLMDeployBase``, based on the inference capabilities provided by the [VLLM](https://github.com/vllm-project/vllm) framework, used for inference with large language models.

Args:
    trust_remote_code (bool): Whether to allow loading of model code from remote servers, default is ``True``.
    launcher (lazyllm.launcher): The launcher for fine-tuning, default is ``launchers.remote(ngpus=1)``.
    stream (bool): Whether the response is streaming, default is ``False``.
    kw: Keyword arguments used to update default training parameters. Note that not any additional keyword arguments can be specified here.

''')

add_example('deploy.Vllm', '''\
>>> from lazyllm import deploy
>>> infer = deploy.vllm()
''')

# Deploy-Auto
add_chinese_doc('auto.AutoDeploy', '''\
此类是 ``LazyLLMDeployBase`` 的子类，可根据输入的参数自动选择合适的推理框架和参数，以对大语言模型进行推理。

具体而言，基于输入的：``base_model`` 的模型参数、``max_token_num``、``launcher`` 中GPU的类型以及卡数，该类可以自动选择出合适的推理框架（如: ``Lightllm`` 或 ``Vllm``）及所需的参数。

Args:
    base_model (str): 用于进行微调的基模型，要求是基模型的路径或模型名。用于提供基模型信息。
    source (lazyllm.config['model_source']): 指定模型的下载源。可通过设置环境变量 ``LAZYLLM_MODEL_SOURCE`` 来配置，目前仅支持 ``huggingface`` 或 ``modelscope`` 。若不设置，lazyllm不会启动自动模型下载。
    trust_remote_code (bool): 是否允许加载来自远程服务器的模型代码，默认为 ``True``。
    launcher (lazyllm.launcher): 微调的启动器，默认为 ``launchers.remote(ngpus=1)``。
    stream (bool): 是否为流式响应，默认为 ``False``。
    type (str): 类型参数，默认为 ``None``，及``llm``类型，另外还支持``embed``类型。
    max_token_num (int): 输入微调模型的token最大长度，默认为``1024``。
    launcher (lazyllm.launcher): 微调的启动器，默认为 ``launchers.remote(ngpus=1)``。
    kw: 关键字参数，用于更新默认的训练参数。注意这里能够指定的关键字参数取决于 LazyLLM 推测出的框架，因此建议谨慎设置。

''')

add_english_doc('auto.AutoDeploy', '''\
This class is a subclass of ``LazyLLMDeployBase`` that automatically selects the appropriate inference framework and parameters based on the input arguments for inference with large language models.

Specifically, based on the input ``base_model`` parameters, ``max_token_num``, the type and number of GPUs in ``launcher``, this class can automatically select the appropriate inference framework (such as ``Lightllm`` or ``Vllm``) and the required parameters.

Args:
    base_model (str): The base model for fine-tuning, which is required to be the name or the path to the base model. Used to provide base model information.
    source (lazyllm.config['model_source']): Specifies the model download source. This can be configured by setting the environment variable ``LAZYLLM_MODEL_SOURCE``.
    trust_remote_code (bool): Whether to allow loading of model code from remote servers, default is ``True``.
    launcher (lazyllm.launcher): The launcher for fine-tuning, default is ``launchers.remote(ngpus=1)``.
    stream (bool): Whether the response is streaming, default is ``False``.
    type (str): Type parameter, default is ``None``, which corresponds to the ``llm`` type. Additionally, the ``embed`` type is also supported.
    max_token_num (int): The maximum token length for the input fine-tuning model, default is ``1024``.
    launcher (lazyllm.launcher): The launcher for fine-tuning, default is ``launchers.remote(ngpus=1)``.
    kw: Keyword arguments used to update default training parameters. Note that whether additional keyword arguments can be specified depends on the framework inferred by LazyLLM, so it is recommended to set them carefully.

''')

add_example('auto.AutoDeploy', '''\
>>> from lazyllm import deploy
>>> deploy.auto('Llama-7b')
<lazyllm.llm.deploy type=Vllm>    
''')

add_chinese_doc('ModelManager', '''\
ModelManager是LazyLLM为开发者提供的自动下载模型的工具类。目前支持从一个本地目录列表查找指定模型，以及从huggingface或者modelscope自动下载模型数据至指定目录。
在使用ModelManager之前，需要设置下列环境变量：

    - LAZYLLM_MODEL_SOURCE: 模型下载源，可以设置为 ``huggingface`` 或 ``modelscope`` 。
    - LAZYLLM_MODEL_SOURCE_TOKEN: ``huggingface`` 或 ``modelscope`` 提供的token，用于下载私有模型。
    - LAZYLLM_MODEL_PATH: 冒号 ``:`` 分隔的本地绝对路径列表用于搜索模型。
    - LAZYLLM_MODEL_CACHE_DIR: 下载后的模型在本地的存储目录

ModelManager.download(model) -> str

用于从model_source下载模型。download函数首先在ModelManager类初始化参数model_path列出的目录中搜索目标模型。如果未找到，会在cache_dir下搜索目标模型。如果仍未找到，
则从model_source上下载模型并存放于cache_dir下。

Args:
    model (str): 目标模型名称。download函数使用此名称从model_source上下载模型。为了方便开发者使用，LazyLLM为常用模型建立了简略模型名称到下载源实际模型名称的映射，
        例如 ``Llama-3-8B`` , ``GLM3-6B`` 或 ``Qwen1.5-7B`` 。具体可参考文件 ``lazyllm/module/utils/downloader/model_mapping.py`` 。model可以接受简略模型名或下载源中的模型全名。
''')

add_english_doc('ModelManager', '''\
ModelManager is a utility class provided by LazyLLM for developers to automatically download models.
Currently, it supports search for models from local directories, as well as automatically downloading model from
huggingface or modelscope. Before using ModelManager, the following environment variables need to be set:

    - LAZYLLM_MODEL_SOURCE: The source for model downloads, which can be set to ``huggingface`` or ``modelscope`` .
    - LAZYLLM_MODEL_SOURCE_TOKEN: The token provided by ``huggingface`` or ``modelscope`` for private model download.
    - LAZYLLM_MODEL_PATH: A colon-separated ``:`` list of local absolute paths for model search.
    - LAZYLLM_MODEL_CACHE_DIR: Directory for downloaded models.

ModelManager.download(model) -> str

Download models from model_source. The function first searches for the target model in directories listed in the
model_path parameter of ModelManager class. If not found, it searches under cache_dir. If still not found,
it downloads the model from model_source and stores it under cache_dir.

Args:
    model (str): The name of the target model. The function uses this name to download the model from model_source.
    To further simplify use of the function, LazyLLM provides a mapping dict from abbreviated model names to original
    names on the download source for popular models, such as ``Llama-3-8B`` , ``GLM3-6B`` or ``Qwen1.5-7B``. For more details,
    please refer to the file ``lazyllm/module/utils/downloader/model_mapping.py`` . The model argument can be either
    an abbreviated name or one from the download source.
''')

add_example('ModelManager', '''\
>>> from lazyllm.components import ModelManager
>>> downloader = ModelManager(model_source='modelscope')
>>> downloader.download('GLM3-6B')
''')

# ============= Formatter

# FormatterBase
add_chinese_doc('formatter.FormatterBase', '''\
此类是格式化器的基类，格式化器是模型输出结果的格式化器，用户可以自定义格式化器，也可以使用LazyLLM提供的格式化器。
主要方法：_parse_formatter:解析索引内容。_load:解析str对象，其中包含python对象的部分被解析出来，比如list，dict等对象。_parse_py_data_by_formatter:根据自定义的格式化器和索引对python对象进行格式化。format:对传入的内容进行格式化，如果内容是字符串类型，先将字符串转化为python对象，再进行格式化。如果内容是python对象，直接进行格式化。
''')

add_english_doc('formatter.FormatterBase', '''\
This class is the base class of the formatter. The formatter is the formatter of the model output result. Users can customize the formatter or use the formatter provided by LazyLLM.
Main methods: _parse_formatter: parse the index content. _load: Parse the str object, and the part containing Python objects is parsed out, such as list, dict and other objects. _parse_py_data_by_formatter: format the python object according to the custom formatter and index. format: format the passed content. If the content is a string type, convert the string into a python object first, and then format it. If the content is a python object, format it directly.
''')

add_example('formatter.FormatterBase', '''\
>>> from lazyllm.components.formatter import FormatterBase
>>> class MyFormatter(LazyLLMFormatterBase):
...    def _load(self, data):
...        return str_to_list(data)
...
...    def _parse_py_data_by_formatter(self, data, formatter):
...        return extract_data_by_formatter(data, formatter)
...
>>> fmt = MyFormatter("[1:3]") # 取列表中索引为1和2的元素
>>> fmt.format("[1,2,3,4,5]") # 输入为字符串"[1,2,3,4,5]"
[2,3]
''')

# JsonFormatter
add_chinese_doc('JsonFormatter', '''\
此类是JSON格式化器，即用户希望模型输出的内容格式为JSON，还可以通过索引方式对输出内容中的某个字段进行选择。
''')

add_english_doc('JsonFormatter', '''\
This class is a JSON formatter, that is, the user wants the model to output content is JSON format, and can also select a field in the output content by indexing.
''')

add_example('JsonFormatter', '''\
>>> from lazyllm.components import JsonFormatter
>>> # Assume that the model output without specifying a formatter is as follows:
"Based on your input, here is the corresponding list of nested dictionaries:\\\\n\\\\n```python\\\\n[\\\\n    {\\\\n        \\\"title\\\": \\\"# Introduction\\\",\\\\n        \\\"describe\\\": \\\"Provide an overview of the topic and set the stage for the article. Discuss what the reader can expect to learn from this article.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"## What is Artificial Intelligence?\\\",\\\\n        \\\"describe\\\": \\\"Define Artificial Intelligence and discuss its importance in various fields, including the medical industry.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"## Applications of AI in Medical Field\\\",\\\\n        \\\"describe\\\": \\\"Outline the ways AI is used in the medical field, such as diagnosis, drug discovery, and patient treatment.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"### Medical Image Analysis\\\",\\\\n        \\\"describe\\\": \\\"Discuss how AI-powered image analysis tools help in detecting diseases and analyzing medical images, such as X-rays, MRIs, and CT scans.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"### Personalized Medicine\\\",\\\\n        \\\"describe\\\": \\\"Explain how AI algorithms can assist in genetic testing and tailor treatment plans based on an individual's genetic makeup.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"### Electronic Health Records (EHRs) and Medical Data Management\\\",\\\\n        \\\"describe\\\": \\\"Discuss the role of AI in managing and analyzing large amounts of medical data, such as electronic health records, for improved patient care and population health management.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"## Challenges in AI Adoption\\\",\\\\n        \\\"describe\\\": \\\"Highlight potential challenges to AI implementation, including data privacy, ethical concerns, and regulatory issues.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"## Future of AI in Medicine\\\",\\\\n        \\\"describe\\\": \\\"Investigate the evolving role of AI in medicine, the anticipated advancements in the field, and their potential impact on medical professionals and patients.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"# Conclusion\\\",\\\\n        \\\"describe\\\": \\\"Summarize the key points of the article and emphasize the potential for AI in revolutionizing the medical field.\\\"\\\\n    }\\\\n]\\\\n```\\\\n\\\\nPlease use the provided `title` and `describe` information to write your article, leveraging Markdown format to denote hierarchical levels. Each `title` should reflect its corresponding level in a Markdown format, including \\\"#\\\" for level 1, \\\"##\\\" for level 2, and \"###\" for level 3. The `describe` text provides a guide for developing each section of the article, ensuring it aligns with the overarching discussion on the application of AI in the medical field."
>>> jsonFormatter=JsonFormatter("[:, title]")  # ":" represents all elements in a list. "title" represents the "title" field in the json data.
>>> model.formatter(jsonFormatter)
>>> # The model output of the specified formatter is as follows
["# Introduction", "## What is Artificial Intelligence?", "## Applications of AI in Medical Field", "### Medical Image Analysis", "### Personalized Medicine", "### Electronic Health Records (EHRs) and Medical Data Management", "## Challenges in AI Adoption", "## Future of AI in Medicine", "# Conclusion"]
''')

# EmptyFormatter
add_chinese_doc('EmptyFormatter', '''\
此类是空的格式化器，即用户希望对模型的输出不做格式化，用户可以对模型指定该格式化器，也可以不指定(模型默认的格式化器就是空格式化器)
''')

add_english_doc('EmptyFormatter', '''\
This type is the system default formatter. When the user does not specify anything or does not want to format the model output, this type is selected. The model output will be in the same format.
''')

add_example('EmptyFormatter', '''\
>>> from lazyllm.components import EmptyFormatter
>>> # Assume that the model output without specifying a formatter is as follows:
"Here's a nested list of dictionaries based on your user input:\\\\n\\\\n```json\\\\n[\\\\n    {\\\\n        \\\"title\\\": \\\"# AI in Medical Field\\\",\\\\n        \\\"describe\\\": \\\"Please provide a detailed introduction to the use of artificial intelligence in the medical field, emphasizing its potential benefits and challenges.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"## Applications of AI in Medical Diagnosis\\\",\\\\n        \\\"describe\\\": \\\"Please discuss the utilization of AI in medical diagnosis, including its advantages over traditional methods and notable achievements.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"### AI-assisted Diagnosis Tools\\\",\\\\n        \\\"describe\\\": \\\"Please elaborate on specific AI-assisted diagnostic tools used in medical practice, such as image analysis, predictive analytics, and decision support systems.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"#### Image Analysis Tools\\\",\\\\n        \\\"describe\\\": \\\"Please provide a comprehensive overview of AI-powered image analysis tools and their role in enhancing disease detection and treatment planning.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"#### Predictive Analytics\\\",\\\\n        \\\"describe\\\": \\\"Please explain how predictive analytics leverages AI to forecast diseases, identify risk factors, and develop personalized treatment protocols.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"#### Decision Support Systems\\\",\\\\n        \\\"describe\\\": \\\"Please discuss the role of decision support systems in facilitating clinical decision-making and improving patient outcomes.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"## Advantages and Limitations of AI in Medical Field\\\",\\\\n        \\\"describe\\\": \\\"Please identify and elaborate on the key advantages and limitations of employing AI in the medical field, including ethical, legal, and practical considerations.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"## Future Perspectives and Innovations\\\",\\\\n        \\\"describe\\\": \\\"Please provide a forward-looking view of the progression of AI in the healthcare sector, predicting future developments, and discussing the potential impact on medical professionals and patients.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"### New AI Technologies\\\",\\\\n        \\\"describe\\\": \\\"Please discuss emerging AI technologies that could reshape the medical field, such as machine learning, natural language processing, and robotics.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"#### Machine Learning\\\",\\\\n        \\\"describe\\\": \\\"Please explain how machine learning algorithms are being used to enhance medical research, such as in drug discovery, genomics, and epidemiology.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"#### Natural Language Processing\\\",\\\\n        \\\"describe\\\": \\\"Please discuss the role of natural language processing in extracting and analyzing medical data from various sources, such as electronic health records and scientific literature.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"#### Robotics\\\",\\\\n        \\\"describe\\\": \\\"Please elaborate on the incorporation of AI-driven robots in medical procedures and surgeries, emphasizing their potential to revolutionize patient care and treatment options.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"### Ethical Considerations\\\",\\\\n        \\\"describe\\\": \\\"Please address the ethical concerns surrounding AI in healthcare, such as data privacy, transparency, and patient autonomy, and discuss potential methods to mitigate these issues.\\\"\\\\n    }\\\\n]\\\\n```\\\\n\\\\nThis outline provides a comprehensive structure for your article, addressing various aspects of the application of AI in the medical field, from specific AI technologies to ethical considerations. You can start by elaborating on each section, providing detailed descriptions, examples, and relevant information. Be sure to include scientific research, case studies, and expert opinions to support your arguments and provide a comprehensive understanding of the subject."
>>> emptyFormatter = EmptyFormatter()
>>> model.formatter(emptyFormatter)
>>> # The model output of the specified formatter is as follows
"Here's a nested list of dictionaries based on your user input:\\\\n\\\\n```json\\\\n[\\\\n    {\\\\n        \\\"title\\\": \\\"# AI in Medical Field\\\",\\\\n        \\\"describe\\\": \\\"Please provide a detailed introduction to the use of artificial intelligence in the medical field, emphasizing its potential benefits and challenges.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"## Applications of AI in Medical Diagnosis\\\",\\\\n        \\\"describe\\\": \\\"Please discuss the utilization of AI in medical diagnosis, including its advantages over traditional methods and notable achievements.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"### AI-assisted Diagnosis Tools\\\",\\\\n        \\\"describe\\\": \\\"Please elaborate on specific AI-assisted diagnostic tools used in medical practice, such as image analysis, predictive analytics, and decision support systems.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"#### Image Analysis Tools\\\",\\\\n        \\\"describe\\\": \\\"Please provide a comprehensive overview of AI-powered image analysis tools and their role in enhancing disease detection and treatment planning.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"#### Predictive Analytics\\\",\\\\n        \\\"describe\\\": \\\"Please explain how predictive analytics leverages AI to forecast diseases, identify risk factors, and develop personalized treatment protocols.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"#### Decision Support Systems\\\",\\\\n        \\\"describe\\\": \\\"Please discuss the role of decision support systems in facilitating clinical decision-making and improving patient outcomes.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"## Advantages and Limitations of AI in Medical Field\\\",\\\\n        \\\"describe\\\": \\\"Please identify and elaborate on the key advantages and limitations of employing AI in the medical field, including ethical, legal, and practical considerations.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"## Future Perspectives and Innovations\\\",\\\\n        \\\"describe\\\": \\\"Please provide a forward-looking view of the progression of AI in the healthcare sector, predicting future developments, and discussing the potential impact on medical professionals and patients.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"### New AI Technologies\\\",\\\\n        \\\"describe\\\": \\\"Please discuss emerging AI technologies that could reshape the medical field, such as machine learning, natural language processing, and robotics.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"#### Machine Learning\\\",\\\\n        \\\"describe\\\": \\\"Please explain how machine learning algorithms are being used to enhance medical research, such as in drug discovery, genomics, and epidemiology.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"#### Natural Language Processing\\\",\\\\n        \\\"describe\\\": \\\"Please discuss the role of natural language processing in extracting and analyzing medical data from various sources, such as electronic health records and scientific literature.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"#### Robotics\\\",\\\\n        \\\"describe\\\": \\\"Please elaborate on the incorporation of AI-driven robots in medical procedures and surgeries, emphasizing their potential to revolutionize patient care and treatment options.\\\"\\\\n    },\\\\n    {\\\\n        \\\"title\\\": \\\"### Ethical Considerations\\\",\\\\n        \\\"describe\\\": \\\"Please address the ethical concerns surrounding AI in healthcare, such as data privacy, transparency, and patient autonomy, and discuss potential methods to mitigate these issues.\\\"\\\\n    }\\\\n]\\\\n```\\\\n\\\\nThis outline provides a comprehensive structure for your article, addressing various aspects of the application of AI in the medical field, from specific AI technologies to ethical considerations. You can start by elaborating on each section, providing detailed descriptions, examples, and relevant information. Be sure to include scientific research, case studies, and expert opinions to support your arguments and provide a comprehensive understanding of the subject."
''')

# ============= Prompter

add_chinese_doc('prompter.PrompterBase', '''\
Prompter的基类，自定义的Prompter需要继承此基类，并通过基类提供的 ``_init_prompt`` 函数来设置Prompt模板和Instruction的模板，以及截取结果所使用的字符串。可以查看 :[prompt](/Best%20Practice/prompt) 进一步了解Prompt的设计思想和使用方式。

Prompt模板和Instruction模板都用 ``{}`` 表示要填充的字段，其中Prompt可包含的字段有 ``system``, ``history``, ``tools``, ``user`` 等，而instruction_template可包含的字段为 ``instruction`` 和 ``extro_keys`` 。
``instruction`` 由应用的开发者传入， ``instruction`` 中也可以带有 ``{}`` 用于让定义可填充的字段，方便用户填入额外的信息。如果 ``instruction`` 字段为字符串，则认为是系统instruction；如果是字典，则它包含的key只能是 ``user`` 和 ``system`` 两种选择。 ``user`` 表示用户输入的instruction，在prompt中放在用户输入前面， ``system`` 表示系统instruction，在prompt中凡在system prompt后面。
''')

add_english_doc('prompter.PrompterBase', '''\
The base class of Prompter. A custom Prompter needs to inherit from this base class and set the Prompt template and the Instruction template using the `_init_prompt` function provided by the base class, as well as the string used to capture results. Refer to  [prompt](/Best%20Practice/prompt) for further understanding of the design philosophy and usage of Prompts.

Both the Prompt template and the Instruction template use ``{}`` to indicate the fields to be filled in. The fields that can be included in the Prompt are `system`, `history`, `tools`, `user` etc., while the fields that can be included in the instruction_template are `instruction` and `extro_keys`. If the ``instruction`` field is a string, it is considered as a system instruction; if it is a dictionary, it can only contain the keys ``user`` and ``system``. ``user`` represents the user input instruction, which is placed before the user input in the prompt, and ``system`` represents the system instruction, which is placed after the system prompt in the prompt.
``instruction`` is passed in by the application developer, and the ``instruction`` can also contain ``{}`` to define fillable fields, making it convenient for users to input additional information.
''')

add_example('prompter.PrompterBase', '''\
>>> from lazyllm.components.prompter import PrompterBase
>>> class MyPrompter(PrompterBase):
...     def __init__(self, instruction = None, extro_keys = None, show = False):
...         super(__class__, self).__init__(show)
...         instruction_template = f'{instruction}\\\\n{{extro_keys}}\\\\n'.replace('{extro_keys}', PrompterBase._get_extro_key_template(extro_keys))
...         self._init_prompt("<system>{system}</system>\\\\n</instruction>{instruction}</instruction>{history}\\\\n{input}\\\\n, ## Response::", instruction_template, '## Response::')
... 
>>> p = MyPrompter('ins {instruction}')
>>> p.generate_prompt('hello')
'<system>You are an AI-Agent developed by LazyLLM.</system>\\\\n</instruction>ins hello\\\\n\\\\n</instruction>\\\\n\\\\n, ## Response::'
>>> p.generate_prompt('hello world', return_dict=True)
{'messages': [{'role': 'system', 'content': 'You are an AI-Agent developed by LazyLLM.\\\\nins hello world\\\\n\\\\n'}, {'role': 'user', 'content': ''}]}
''')

add_chinese_doc('prompter.PrompterBase.generate_prompt', '''\
根据用户输入，生成对应的Prompt.

Args:
    input (Option[str | Dict]):  Prompter的输入，如果是dict，会填充到instruction的槽位中；如果是str，则会作为输入。
    history (Option[List[List | Dict]]): 历史对话，可以为 ``[[u, s], [u, s]]`` 或 openai的history格式，默认为None。
    tools (Option[List[Dict]]: 可以使用的工具合集，大模型用作FunctionCall时使用，默认为None
    label (Option[str]): 标签，训练或微调时使用，默认为None
    show (bool): 标志是否打印生成的Prompt，默认为False
    return_dict (bool): 标志是否返回dict，一般情况下使用 ``OnlineChatModule`` 时会设置为True。如果返回dict，则仅填充 ``instruction``。默认为False
''')

add_english_doc('prompter.PrompterBase.generate_prompt', '''\

Generate a corresponding Prompt based on user input.

Args:
    input (Option[str | Dict]): The input from the prompter, if it's a dict, it will be filled into the slots of the instruction; if it's a str, it will be used as input.
    history (Option[List[List | Dict]]): Historical conversation, can be ``[[u, s], [u, s]]`` or in openai's history format, defaults to None.
    tools (Option[List[Dict]]): A collection of tools that can be used, used when the large model performs FunctionCall, defaults to None.
    label (Option[str]): Label, used during fine-tuning or training, defaults to None.
    show (bool): Flag indicating whether to print the generated Prompt, defaults to False.
    return_dict (bool): Flag indicating whether to return a dict, generally set to True when using ``OnlineChatModule``. If returning a dict, only the ``instruction`` will be filled. Defaults to False.
''')

add_chinese_doc('prompter.PrompterBase.get_response', '''\
用作对Prompt的截断，只保留有价值的输出

Args:
     output (str): 大模型的输出
     input (Option[[str]): 大模型的输入，若指定此参数，会将输出中包含输入的部分全部截断，默认为None
''')

add_english_doc('prompter.PrompterBase.get_response', '''\
Used to truncate the Prompt, keeping only valuable output.

Args:
        output (str): The output of the large model.
        input (Option[str]): The input of the large model. If this parameter is specified, any part of the output that includes the input will be completely truncated. Defaults to None.
''')

add_chinese_doc('AlpacaPrompter', '''\
Alpaca格式的Prompter，支持工具调用，不支持历史对话。

Args:
    instruction (Option[str]): 大模型的任务指令，至少带一个可填充的槽位(如 ``{instruction}``)。或者使用字典指定 ``system`` 和 ``user`` 的指令。
    extro_keys (Option[List]): 额外的字段，用户的输入会填充这些字段。
    show (bool): 标志是否打印生成的Prompt，默认为False
    tools (Option[list]): 大模型可以使用的工具集合，默认为None
''')

add_english_doc('AlpacaPrompter', '''\
Alpaca-style Prompter, supports tool calls, does not support historical dialogue.

Sure! Here is the translation, keeping the original format:

Args:
    instruction (Option[str]): Task instructions for the large model, with at least one fillable slot (e.g. ``{instruction}``). Or use a dictionary to specify the ``system`` and ``user`` instructions.
    extro_keys (Option[List]): Additional fields that will be filled with user input.
    show (bool): Flag indicating whether to print the generated Prompt, default is False.
    tools (Option[list]): Tool-set which is provived for LLMs, default is None.
''')

add_example('AlpacaPrompter', '''\
>>> from lazyllm import AlpacaPrompter
>>> p = AlpacaPrompter('hello world {instruction}')
>>> p.generate_prompt('this is my input')
'You are an AI-Agent developed by LazyLLM.\\\\nBelow is an instruction that describes a task, paired with extra messages such as input that provides further context if possible. Write a response that appropriately completes the request.\\\\n\\\\n ### Instruction:\\\\nhello world this is my input\\\\n\\\\n\\\\n### Response:\\\\n'
>>> p.generate_prompt('this is my input', return_dict=True)
{'messages': [{'role': 'system', 'content': 'You are an AI-Agent developed by LazyLLM.\\\\nBelow is an instruction that describes a task, paired with extra messages such as input that provides further context if possible. Write a response that appropriately completes the request.\\\\n\\\\n ### Instruction:\\\\nhello world this is my input\\\\n\\\\n'}, {'role': 'user', 'content': ''}]}
>>>
>>> p = AlpacaPrompter('hello world {instruction}, {input}', extro_keys=['knowledge'])
>>> p.generate_prompt(dict(instruction='hello world', input='my input', knowledge='lazyllm'))
'You are an AI-Agent developed by LazyLLM.\\\\nBelow is an instruction that describes a task, paired with extra messages such as input that provides further context if possible. Write a response that appropriately completes the request.\\\\n\\\\n ### Instruction:\\\\nhello world hello world, my input\\\\n\\\\nHere are some extra messages you can referred to:\\\\n\\\\n### knowledge:\\\\nlazyllm\\\\n\\\\n\\\\n### Response:\\\\n'
>>> p.generate_prompt(dict(instruction='hello world', input='my input', knowledge='lazyllm'), return_dict=True)
{'messages': [{'role': 'system', 'content': 'You are an AI-Agent developed by LazyLLM.\\\\nBelow is an instruction that describes a task, paired with extra messages such as input that provides further context if possible. Write a response that appropriately completes the request.\\\\n\\\\n ### Instruction:\\\\nhello world hello world, my input\\\\n\\\\nHere are some extra messages you can referred to:\\\\n\\\\n### knowledge:\\\\nlazyllm\\\\n\\\\n'}, {'role': 'user', 'content': ''}]}
>>> 
>>> p = AlpacaPrompter(dict(system="hello world", user="this is user instruction {input}"))
>>> p.generate_prompt(dict(input="my input"))
'You are an AI-Agent developed by LazyLLM.\\\\nBelow is an instruction that describes a task, paired with extra messages such as input that provides further context if possible. Write a response that appropriately completes the request.\\\\n\\\\n ### Instruction:\\\\nhello word\\\\n\\\\n\\\\n\\\\nthis is user instruction my input### Response:\\\\n'
>>> p.generate_prompt(dict(input="my input"), return_dict=True)
{'messages': [{'role': 'system', 'content': 'You are an AI-Agent developed by LazyLLM.\\\\nBelow is an instruction that describes a task, paired with extra messages such as input that provides further context if possible. Write a response that appropriately completes the request.\\\\n\\\\n ### Instruction:\\\\nhello world'}, {'role': 'user', 'content': 'this is user instruction my input'}]}

''')

add_chinese_doc('ChatPrompter', '''\
多轮对话的Prompt，支持工具调用和历史对话

Args:
    instruction (Option[str]): 大模型的任务指令，可以带0到多个待填充的槽位,用 ``{}`` 表示。针对用户instruction可以通过字典传递，字段为 ``user`` 和 ``system`` 。
    extro_keys (Option[List]): 额外的字段，用户的输入会填充这些字段。
    show (bool): 标志是否打印生成的Prompt，默认为False
''')

add_english_doc('ChatPrompter', '''\
chat prompt, supports tool calls and historical dialogue.

Args:
    instruction (Option[str]): Task instructions for the large model, with 0 to multiple fillable slot, represented by ``{}``. For user instructions, you can pass a dictionary with fields ``user`` and ``system``.
    extro_keys (Option[List]): Additional fields that will be filled with user input.
    show (bool): Flag indicating whether to print the generated Prompt, default is False.
''')

add_example('ChatPrompter', '''\
>>> from lazyllm import ChatPrompter
>>> p = ChatPrompter('hello world')
>>> p.generate_prompt('this is my input')
'<|start_system|>You are an AI-Agent developed by LazyLLM.hello world\\\\n\\\\n<|end_system|>\\\\n\\\\n\\\\n<|Human|>:\\\\nthis is my input\\\\n<|Assistant|>:\\\\n'
>>> p.generate_prompt('this is my input', return_dict=True)
{'messages': [{'role': 'system', 'content': 'You are an AI-Agent developed by LazyLLM.\\\\nhello world\\\\n\\\\n'}, {'role': 'user', 'content': 'this is my input'}]}
>>>
>>> p = ChatPrompter('hello world {instruction}', extro_keys=['knowledge'])
>>> p.generate_prompt(dict(instruction='this is my ins', input='this is my inp', knowledge='LazyLLM-Knowledge'))
'<|start_system|>You are an AI-Agent developed by LazyLLM.hello world this is my ins\\\\nHere are some extra messages you can referred to:\\\\n\\\\n### knowledge:\\\\nLazyLLM-Knowledge\\\\n\\\\n\\\\n<|end_system|>\\\\n\\\\n\\\\n<|Human|>:\\\\nthis is my inp\\\\n<|Assistant|>:\\\\n'
>>> p.generate_prompt(dict(instruction='this is my ins', input='this is my inp', knowledge='LazyLLM-Knowledge'), return_dict=True)
{'messages': [{'role': 'system', 'content': 'You are an AI-Agent developed by LazyLLM.\\\\nhello world this is my ins\\\\nHere are some extra messages you can referred to:\\\\n\\\\n### knowledge:\\\\nLazyLLM-Knowledge\\\\n\\\\n\\\\n'}, {'role': 'user', 'content': 'this is my inp'}]}
>>> p.generate_prompt(dict(instruction='this is my ins', input='this is my inp', knowledge='LazyLLM-Knowledge'), history=[['s1', 'e1'], ['s2', 'e2']])
'<|start_system|>You are an AI-Agent developed by LazyLLM.hello world this is my ins\\\\nHere are some extra messages you can referred to:\\\\n\\\\n### knowledge:\\\\nLazyLLM-Knowledge\\\\n\\\\n\\\\n<|end_system|>\\\\n\\\\n<|Human|>:s1<|Assistant|>:e1<|Human|>:s2<|Assistant|>:e2\\\\n<|Human|>:\\\\nthis is my inp\\\\n<|Assistant|>:\\\\n'
>>>
>>> p = ChatPrompter(dict(system="hello world", user="this is user instruction {input} "))
>>> p.generate_prompt(dict(input="my input", query="this is user query"))
'<|start_system|>You are an AI-Agent developed by LazyLLM.hello world\\\\n\\\\n<|end_system|>\\\\n\\\\n\\\\n<|Human|>:\\\\nthis is user instruction my input this is user query\\\\n<|Assistant|>:\\\\n'
>>> p.generate_prompt(dict(input="my input", query="this is user query"), return_dict=True)
{'messages': [{'role': 'system', 'content': 'You are an AI-Agent developed by LazyLLM.\\\\nhello world\\\\n\\\\n'}, {'role': 'user', 'content': 'this is user instruction my input this is user query'}]}
''')

# ============= Launcher

add_chinese_doc = functools.partial(utils.add_chinese_doc, module=lazyllm.launcher)
add_english_doc = functools.partial(utils.add_english_doc, module=lazyllm.launcher)
add_example = functools.partial(utils.add_example, module=lazyllm.launcher)

# Launcher-EmptyLauncher
add_chinese_doc('EmptyLauncher', '''\
此类是 ``LazyLLMLaunchersBase`` 的子类，作为一个本地的启动器。

Args:
    subprocess (bool): 是否使用子进程来启动。默认为 `False`。
    sync (bool): 是否同步执行作业。默认为 `True`，否则为异步执行。

''')

add_english_doc('EmptyLauncher', '''\
This class is a subclass of ``LazyLLMLaunchersBase`` and serves as a local launcher.

Args:
    subprocess (bool): Whether to use a subprocess to launch. Default is ``False``.
    sync (bool): Whether to execute jobs synchronously. Default is ``True``, otherwise it executes asynchronously.

''')

add_example('EmptyLauncher', '''\
>>> import lazyllm
>>> launcher = lazyllm.launchers.empty()
''')

# Launcher-SlurmLauncher
add_chinese_doc('SlurmLauncher', '''\
此类是 ``LazyLLMLaunchersBase`` 的子类，作为slurm启动器。

具体而言，它提供了启动和配置 Slurm 作业的方法，包括指定分区、节点数量、进程数量、GPU 数量以及超时时间等参数。

Args:
    partition (str): 要使用的 Slurm 分区。默认为 ``None``，此时将使用 ``lazyllm.config['partition']`` 中的默认分区。该配置可通过设置环境变量来生效，如 ``export LAZYLLM_SLURM_PART=a100`` 。
    nnode  (int): 要使用的节点数量。默认为 ``1``。
    nproc (int): 每个节点要使用的进程数量。默认为 ``1``。
    ngpus: (int): 每个节点要使用的 GPU 数量。默认为 ``None``, 即不使用 GPU。
    timeout (int): 作业的超时时间（以秒为单位）。默认为 ``None``，此时将不设置超时时间。
    sync (bool): 是否同步执行作业。默认为 ``True``，否则为异步执行。

''')

add_english_doc('SlurmLauncher', '''\
This class is a subclass of ``LazyLLMLaunchersBase`` and acts as a Slurm launcher.

Specifically, it provides methods to start and configure Slurm jobs, including specifying parameters such as the partition, number of nodes, number of processes, number of GPUs, and timeout settings.

Args:
    partition (str): The Slurm partition to use. Defaults to ``None``, in which case the default partition in ``lazyllm.config['partition']`` will be used. This configuration can be enabled by setting environment variables, such as ``export LAZYLLM_SLURM_PART=a100``.
    nnode  (int): The number of nodes to use. Defaults to ``1``.
    nproc (int): The number of processes per node. Defaults to ``1``.
    ngpus (int): The number of GPUs per node. Defaults to ``None``, meaning no GPUs will be used.
    timeout (int): The timeout for the job in seconds. Defaults to ``None``, in which case no timeout will be set.
    sync (bool): Whether to execute the job synchronously. Defaults to ``True``, otherwise it will be executed asynchronously.

''')

add_example('SlurmLauncher', '''\
>>> import lazyllm
>>> launcher = lazyllm.launchers.slurm(partition='partition_name', nnode=1, nproc=1, ngpus=1, sync=False)
''')

# Launcher-ScoLauncher
add_chinese_doc('ScoLauncher', '''\
此类是 ``LazyLLMLaunchersBase`` 的子类，作为SCO (Sensecore)启动器。

具体而言，它提供了启动和配置 SCO 作业的方法，包括指定分区、工作空间名称、框架类型、节点数量、进程数量、GPU 数量以及是否使用 torchrun 等参数。

Args:
    partition (str): 要使用的分区。默认为 ``None``，此时将使用 ``lazyllm.config['partition']`` 中的默认分区。该配置可通过设置环境变量来生效，如 ``export LAZYLLM_SLURM_PART=a100`` 。
    workspace_name (str): SCO 上的工作空间名称。默认为 ``lazyllm.config['sco.workspace']`` 中的配置。该配置可通过设置环境变量来生效，如 ``export LAZYLLM_SCO_WORKSPACE=myspace`` 。
    framework (str): 要使用的框架类型，例如 ``pt`` 代表 PyTorch。默认为 ``pt``。
    nnode  (int): 要使用的节点数量。默认为 ``1``。
    nproc (int): 每个节点要使用的进程数量。默认为 ``1``。
    ngpus: (int): 每个节点要使用的 GPU 数量。默认为 ``1``, 使用1块 GPU。
    torchrun (bool): 是否使用 ``torchrun`` 启动作业。默认为 ``False``。
    sync (bool): 是否同步执行作业。默认为 ``True``，否则为异步执行。

''')

add_english_doc('ScoLauncher', '''\
This class is a subclass of ``LazyLLMLaunchersBase`` and acts as a SCO launcher.

Specifically, it provides methods to start and configure SCO jobs, including specifying parameters such as the partition, workspace name, framework type, number of nodes, number of processes, number of GPUs, and whether to use torchrun or not.

Args:
    partition (str): The Slurm partition to use. Defaults to ``None``, in which case the default partition in ``lazyllm.config['partition']`` will be used. This configuration can be enabled by setting environment variables, such as ``export LAZYLLM_SLURM_PART=a100``.
    workspace_name (str): The workspace name on SCO. Defaults to the configuration in ``lazyllm.config['sco.workspace']``. This configuration can be enabled by setting environment variables, such as ``export LAZYLLM_SCO_WORKSPACE=myspace``.
    framework (str): The framework type to use, for example, ``pt`` for PyTorch. Defaults to ``pt``.
    nnode  (int): The number of nodes to use. Defaults to ``1``.
    nproc (int): The number of processes per node. Defaults to ``1``.
    ngpus (int): The number of GPUs per node. Defaults to ``1``, using 1 GPU.
    torchrun (bool): Whether to start the job with ``torchrun``. Defaults to ``False``.
    sync (bool): Whether to execute the job synchronously. Defaults to ``True``, otherwise it will be executed asynchronously.

''')

add_example('ScoLauncher', '''\
>>> import lazyllm
>>> launcher = lazyllm.launchers.sco(partition='partition_name', nnode=1, nproc=1, ngpus=1, sync=False)
''')

# Launcher-RemoteLauncher
add_chinese_doc('RemoteLauncher', '''\
此类是 ``LazyLLMLaunchersBase`` 的一个子类，它充当了一个远程启动器的代理。它根据配置文件中的 ``lazyllm.config['launcher']`` 条目动态地创建并返回一个对应的启动器实例(例如：``SlurmLauncher`` 或 ``ScoLauncher``)。

Args:
    *args: 位置参数，将传递给动态创建的启动器构造函数。
    sync (bool): 是否同步执行作业。默认为 ``False``。
    **kwargs: 关键字参数，将传递给动态创建的启动器构造函数。

注意事项: 
    - ``RemoteLauncher`` 不是一个直接的启动器，而是根据配置动态创建一个启动器。 
    - 配置文件中的 ``lazyllm.config['launcher']`` 指定一个存在于 ``lazyllm.launchers`` 模块中的启动器类名。该配置可通过设置环境变量 ``LAZYLLM_DEFAULT_LAUNCHER`` 来设置。如：``export LAZYLLM_DEFAULT_LAUNCHER=sco`` , ``export LAZYLLM_DEFAULT_LAUNCHER=slurm`` 。
''')

add_english_doc('RemoteLauncher', '''\
This class is a subclass of ``LazyLLMLaunchersBase`` and acts as a proxy for a remote launcher. It dynamically creates and returns an instance of the corresponding launcher based on the ``lazyllm.config['launcher']`` entry in the configuration file (for example: ``SlurmLauncher`` or ``ScoLauncher``).

Args:
    *args: Positional arguments that will be passed to the constructor of the dynamically created launcher.
    sync (bool): Whether to execute the job synchronously. Defaults to ``False``.
    **kwargs: Keyword arguments that will be passed to the constructor of the dynamically created launcher.

Notes: 
    - ``RemoteLauncher`` is not a direct launcher but dynamically creates a launcher based on the configuration. 
    - The ``lazyllm.config['launcher']`` in the configuration file specifies a launcher class name present in the ``lazyllm.launchers`` module. This configuration can be set by setting the environment variable ``LAZYLLM_DEAULT_LAUNCHER``. For example: ``export LAZYLLM_DEAULT_LAUNCHER=sco``, ``export LAZYLLM_DEAULT_LAUNCHER=slurm``.

''')

add_example('RemoteLauncher', '''\
>>> import lazyllm
>>> launcher = lazyllm.launchers.remote(ngpus=1)
''')
