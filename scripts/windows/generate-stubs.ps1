$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "../..")
$python = Join-Path $root ".venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    throw "Python not found at $python. Run 'uv sync' first."
}

$protos = Join-Path $root "protos"
$out = Join-Path $root "app\clients\generated"

& $python -m grpc_tools.protoc `
  -I $protos `
  --python_out=$out `
  --grpc_python_out=$out `
  (Join-Path $protos "user\v1\user.proto") `
  (Join-Path $protos "product\v1\product.proto") `
  (Join-Path $protos "order\v1\order.proto")