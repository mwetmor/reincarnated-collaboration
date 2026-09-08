"""Call the actual Blender/Godot MCP servers over stdio from this project."""
import argparse
import asyncio
import base64
import json
import os
from pathlib import Path
from datetime import timedelta
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('server', choices=['blender', 'godot'])
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--tool')
    parser.add_argument('--args-file', type=Path)
    parser.add_argument('--code-file', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--plan', type=Path)
    options = parser.parse_args()
    env = dict(os.environ)
    if options.server == 'blender':
        command = str(ROOT / '.venv/bin/blender-mcp')
        args = []
        env.update(BLENDER_HOST='127.0.0.1', BLENDER_PORT='9877', DISABLE_TELEMETRY='1')
    else:
        command = '/usr/local/bin/node'
        args = ['/Users/admin/Games/vendor/godot-mcp-pro-v1/server/build/index.js']
        env.update(GODOT_PROJECT_PATH=str(ROOT / 'godot'), GODOT_MCP_PORT='6509')
    params = StdioServerParameters(command=command, args=args, env=env, cwd=str(ROOT))
    (ROOT / 'logs').mkdir(exist_ok=True)
    server_log = open(ROOT / 'logs' / f'{options.server}-server.log', 'a')
    async with stdio_client(params, errlog=server_log) as (read, write):
        async with ClientSession(read, write, read_timeout_seconds=timedelta(seconds=180)) as session:
            await session.initialize()
            if options.list:
                result = await session.list_tools()
            else:
                if options.server == 'godot':
                    for _ in range(12):
                        probe = await session.call_tool('get_project_info', {})
                        if 'not connected' not in str(probe).lower():
                            info = json.loads(probe.content[0].text)
                            if Path(info.get('project_path', '')).resolve() != (ROOT / 'godot').resolve():
                                raise RuntimeError('Godot MCP is connected to a different project; refusing to modify it.')
                            break
                        await asyncio.sleep(1)
                    else:
                        raise RuntimeError('Godot MCP did not connect to the wizard project within 12 seconds.')
                if options.plan:
                    records=[]
                    for step in json.loads(options.plan.read_text()):
                        step_args=step.get('args', {})
                        if step.get('code_file'):
                            step_args['code']=Path(step['code_file']).read_text()
                        value=await session.call_tool(step['tool'], step_args)
                        record={'tool':step['tool'],'result':value.model_dump(mode='json',exclude_none=True)}
                        records.append(record)
                        readable=[p.get('text', '[image]') for p in record['result'].get('content', [])]
                        print(step['tool'], '\n'.join(readable)[:1800])
                        if options.output:
                            options.output.write_text(json.dumps(records,indent=2))
                        if value.isError:
                            raise RuntimeError('MCP plan failed at '+step['tool'])
                    return
                args = json.loads(options.args_file.read_text()) if options.args_file else {}
                if options.server == 'blender':
                    args.setdefault('user_prompt', 'Build the purple-and-gold wizard from the supplied references, rig it, and animate it for WASD movement in Godot.')
                if options.code_file:
                    args['code'] = options.code_file.read_text()
                result = await session.call_tool(options.tool, args)
            raw = result.model_dump(mode='json', exclude_none=True)
            (ROOT / 'logs').mkdir(exist_ok=True)
            if options.output:
                options.output.write_text(json.dumps(raw, indent=2))
            if options.list:
                print(json.dumps(raw, indent=2))
            else:
                for i, content in enumerate(raw.get('content', [])):
                    if content['type'] == 'image':
                        path = ROOT / 'logs' / f'{options.server}-capture-{i}.png'
                        path.write_bytes(base64.b64decode(content['data']))
                        print(f'Image: {path}')
                    elif content['type'] == 'text':
                        print(content['text'])
                if raw.get('isError'):
                    raise RuntimeError('MCP tool returned an error')

if __name__ == '__main__':
    asyncio.run(main())
