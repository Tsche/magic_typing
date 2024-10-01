## Design considerations

Main selling point of this preprocessor is that it requires no actual code changes (ie by using decorators) or a different interpreter (ie. cinder, mypyc) to opt in or out of it. Instead a encoding declaration is sufficient. This way strict type checking can quickly be opted into on a per-file basis. 

Unlike projects like cinder or mpypc this preprocessor's intention is not to yield better performance, it is to aid development. 

- no inserted code will be executed if `__debug__` is falsey
If we use assertions or depend on `__debug__`, it is possible to opt out of all inserted checks by running the python interpreter with `-O` or `-O0`.

- all inserted type checks must use assertions
Alternatively `warnings.warn` could be used to emit warnings rather than AssertionError exceptions and therefore only fail hard if the python interpreter is ran with `-Werror`. This might be unintuitive but interesting to explore.

- some form of configuration for the preprocessor might be desired
Specific checks might not be desirable or too expensive for certain use cases. There should be some way to control the behavior of this preprocessor.
-> file scope dictionary constant with special name? We don't want to have to evaluate any actual Python during  preprocessing. Dictionaries of constants would be easy to parse.

- names for all returned or yielded unnamed values must be synthesized if necessary to add type checks
checking the return value type in the function's scope itself generates better diagnostics, especially for functions that contain multiple return/yield statements

- warnings must only be emitted if `__debug__` is truthy (=> easier to opt out of)
- no type checks for anything annotated as Any will be emitted
- type checks for all annotated function parameters must be inserted into the function body
- unannotated functions, function parameters, variables etc in strict file must yield a warning
- dictionary, list and generator comprehensions must be transformed into loops to check every item
TODO: maybe there's a way to place the assertions in the comprehension. Must think about this
- __setattr__ must be hooked for all class types to insert type checks on member change
Theoretically this is in the wrong place and should be at the site of attribute change for better diagnostics. Unfortunately that might prove difficult.

- __setitem__ must be hooked for dictionaries, lists etc. to insert type checks
Same as __setattr__ but much easier to insert at the call site. Inserting at the call site would not require the builtin types to be wrapped or their types patched and would not leak out of the checked file.
- type comments must be respected