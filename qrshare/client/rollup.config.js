import svelte from 'rollup-plugin-svelte';
import commonjs from '@rollup/plugin-commonjs';
import resolve from '@rollup/plugin-node-resolve';
import livereload from 'rollup-plugin-livereload';
import { terser } from 'rollup-plugin-terser';
import css from 'rollup-plugin-css-only';

const production = !process.env.ROLLUP_WATCH;

let bundles = [
	'main',
	'login',
]

function serve() {
	let server;

	function toExit() {
		if (server) server.kill(0);
	}

	return {
		writeBundle() {
			if (server) return;
			server = require('child_process').spawn('npm', ['run', 'start', '--', '--dev'], {
				stdio: ['ignore', 'inherit', 'inherit'],
				shell: true
			});

			process.on('SIGTERM', toExit);
			process.on('exit', toExit);
		}
	};
}

function create({name, flask, singleBundle}) {
	return {
		input: `src/${name}/${name}.js`,
		output: {
			sourcemap: true,
			format: 'iife',
			name: 'app',
			file: `public/build/${name}/bundle.js`
		},
		plugins: [
			svelte({
				compilerOptions: {
					dev: !production
				}
			}),
			css({ output: `bundle.css` }),
	
			resolve({
				browser: true,
				dedupe: ['svelte']
			}),
			commonjs(),
	
			// In dev mode, call `npm run start` once
			// In flask mode, dont serve
			// the bundle has been generated
			!production && !flask && serve(),
			
			!production && (singleBundle
				? livereload(`public`)
				: livereload(`public/build/${name}`)),
	
			// If we're building for production (npm run build
			// instead of npm run dev), minify
			production && terser()
		],
		watch: {
			clearScreen: false
		},
	}
}

export default (args) => {
	// choosing bundles
	for (const name of bundles) {
		if (args[`config-${name}`] === true) {
			bundles = [name]
			break
		}
	}

	const singleBundle = bundles.length === 1
	const flask = args['config-flask'] === true
	const configs = bundles.map((name) => create({name, flask, singleBundle}))

	return configs;
}
