$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "../..")
$python = Join-Path $root ".venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    throw "Python not found at $python. Run 'uv sync' first."
}

$protos = Join-Path $root "protos"
$out = Join-Path $root "app\clients\generated"

# 1) Generate protobuf + grpc python files
& $python -m grpc_tools.protoc `
  -I $protos `
  --python_out=$out `
  --grpc_python_out=$out `
  (Join-Path $protos "user\v1\user.proto") `
  (Join-Path $protos "product\v1\product.proto") `
  (Join-Path $protos "order\v1\order.proto")

if ($LASTEXITCODE -ne 0) {
    throw "protoc generation failed with exit code $LASTEXITCODE"
}

# 2) Ensure package markers exist (__init__.py)
$packageRoots = @(
    $out,
    (Join-Path $out "user"),
    (Join-Path $out "user\v1"),
    (Join-Path $out "product"),
    (Join-Path $out "product\v1"),
    (Join-Path $out "order"),
    (Join-Path $out "order\v1")
)

foreach ($dir in $packageRoots) {
    if (-not (Test-Path $dir)) { continue }
    $init = Join-Path $dir "__init__.py"
    if (-not (Test-Path $init)) {
        New-Item -ItemType File -Path $init | Out-Null
    }
}

# 3) Rewrite generated imports:
# from user.v1 import user_pb2 as ...
# -> from app.clients.generated.user.v1 import user_pb2 as ...
Get-ChildItem $out -Recurse -File | Where-Object { $_.Name -match "_pb2(_grpc)?.py$" } | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $updated = $content -replace `
        'from ([A-Za-z_]\w*)\.v1 import ([A-Za-z_]\w*_pb2(?: as [A-Za-z_]\w*)?)', `
        'from app.clients.generated.$1.v1 import $2'

    if ($updated -ne $content) {
        Set-Content -Path $_.FullName -Value $updated -NoNewline
    }
}

Write-Host "Stub generation complete."